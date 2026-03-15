"""네이버 커머스API 공통 HTTP 클라이언트.

- httpx.AsyncClient 기반
- tenacity로 네트워크 오류 시 최대 3회 재시도 (exponential backoff)
- 401 + GW.AUTHN 시 토큰 자동 재발급 후 재시도
- 에러 응답 → 커스텀 예외 변환
- 로깅: 엔드포인트, 상태코드, 메시지 기록
"""

import logging
from typing import Any

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from auth.token import NaverAuth
from seller.client import SellerClient
from products.client import ProductsClient
from orders.client import OrdersClient
from inquiries.client import InquiriesClient
from logistics.client import LogisticsClient
from exceptions import (
    NaverAPIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://api.commerce.naver.com/external"


class NaverCommerceClient:
    """네이버 커머스API HTTP 클라이언트.

    사용법:
        async with NaverCommerceClient(client_id, client_secret) as client:
            # 판매자 정보 조회
            account = await client.seller.get_account()
    """

    def __init__(self, client_id: str, client_secret: str):
        self.auth = NaverAuth(client_id, client_secret)
        self._http_client: httpx.AsyncClient | None = None
        
        # 서브 클라이언트 초기화
        self.seller = SellerClient(self)
        self.products = ProductsClient(self)
        self.orders = OrdersClient(self)
        self.inquiries = InquiriesClient(self)
        self.logistics = LogisticsClient(self)

    async def __aenter__(self):
        self._http_client = httpx.AsyncClient(
            base_url=BASE_URL,
            timeout=30.0,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None

    async def _get_headers(self) -> dict[str, str]:
        """인증 헤더 생성."""
        token = await self.auth.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _raise_for_error(self, response: httpx.Response) -> None:
        """HTTP 응답이 에러면 커스텀 예외로 변환."""
        if response.status_code < 400:
            return

        body: dict = {}
        try:
            body = response.json()
        except Exception:
            pass

        code = body.get("code", "UNKNOWN")
        message = body.get("message", response.text)
        trace_id = body.get("traceId", "")

        logger.error(
            "API 에러: endpoint=%s, status=%d, code=%s, message=%s",
            response.url,
            response.status_code,
            code,
            message,
        )

        if response.status_code == 401 and code == "GW.AUTHN":
            raise AuthenticationError(
                status_code=response.status_code,
                code=code,
                message=message,
                trace_id=trace_id,
            )
        elif response.status_code == 429:
            raise RateLimitError(
                status_code=response.status_code,
                code=code,
                message=message,
                trace_id=trace_id,
            )
        elif response.status_code == 400:
            raise ValidationError(
                status_code=response.status_code,
                code=code,
                message=message,
                trace_id=trace_id,
            )
        else:
            raise NaverAPIError(
                status_code=response.status_code,
                code=code,
                message=message,
                trace_id=trace_id,
            )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.TransportError,)),
        reraise=True,
    )
    async def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        **kwargs,
    ) -> dict[str, Any] | list | None:
        """HTTP 요청 실행 (재시도 + 토큰 갱신 포함).

        Args:
            method: HTTP 메서드 (GET, POST, PUT, PATCH, DELETE).
            path: API 경로 (예: /v1/seller).
            params: 쿼리 파라미터.
            json_data: JSON 요청 바디.

        Returns:
            응답 JSON 데이터.
        """
        headers = await self._get_headers()

        response = await self._http_client.request(
            method=method,
            url=path,
            params=params,
            json=json_data,
            headers=headers,
            **kwargs,
        )

        # 401 + GW.AUTHN → 토큰 재발급 후 재시도
        if response.status_code == 401:
            body = {}
            try:
                body = response.json()
            except Exception:
                pass
            if body.get("code") == "GW.AUTHN":
                logger.warning("토큰 만료 감지, 재발급 후 재시도")
                self.auth._access_token = None
                self.auth._expires_at = 0
                headers = await self._get_headers()
                response = await self._http_client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json_data,
                    headers=headers,
                    **kwargs,
                )

        self._raise_for_error(response)

        # 204 No Content 등 빈 응답 처리
        if response.status_code == 204 or not response.content:
            return None

        return response.json()

    async def get(self, path: str, params: dict[str, Any] | None = None, **kwargs) -> dict | list | None:
        """GET 요청."""
        return await self._request("GET", path, params=params, **kwargs)

    async def post(self, path: str, json_data: dict[str, Any] | None = None, **kwargs) -> dict | list | None:
        """POST 요청."""
        return await self._request("POST", path, json_data=json_data, **kwargs)

    async def put(self, path: str, json_data: dict[str, Any] | None = None, **kwargs) -> dict | list | None:
        """PUT 요청."""
        return await self._request("PUT", path, json_data=json_data, **kwargs)

    async def patch(self, path: str, json_data: dict[str, Any] | None = None, **kwargs) -> dict | list | None:
        """PATCH 요청."""
        return await self._request("PATCH", path, json_data=json_data, **kwargs)

    async def delete(self, path: str, params: dict[str, Any] | None = None, **kwargs) -> dict | list | None:
        """DELETE 요청."""
        return await self._request("DELETE", path, params=params, **kwargs)
