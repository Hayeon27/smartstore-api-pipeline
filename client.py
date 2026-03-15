"""네이버 커머스API 공통 HTTP 클라이언트."""

import logging
from typing import Any, Dict, List, Optional, TYPE_CHECKING

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
from settlement.client import SettlementClient
from statistics.client import StatisticsClient
from commerce.client import CommerceSolutionClient
from exceptions import (
    NaverAPIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://api.commerce.naver.com/external"


class NaverCommerceClient:
    def __init__(self, client_id: str, client_secret: str):
        self.auth = NaverAuth(client_id, client_secret)
        self._http_client: httpx.AsyncClient | None = None
        
        self.seller = SellerClient(self)
        self.products = ProductsClient(self)
        self.orders = OrdersClient(self)
        self.inquiries = InquiriesClient(self)
        self.logistics = LogisticsClient(self)
        self.settlement = SettlementClient(self)
        self.stats = StatisticsClient(self)
        self.solutions = CommerceSolutionClient(self)

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
        token = await self.auth.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _raise_for_error(self, response: httpx.Response) -> None:
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
            raise AuthenticationError(response.status_code, code, message, trace_id)
        elif response.status_code == 429:
            raise RateLimitError(response.status_code, code, message, trace_id)
        elif response.status_code == 400:
            raise ValidationError(response.status_code, code, message, trace_id)
        else:
            raise NaverAPIError(response.status_code, code, message, trace_id)

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
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        headers = await self._get_headers()
        
        # 디버깅 로깅
        logger.debug(f"[HTTP {method}] {path} | params={params}")

        response = await self._http_client.request(
            method=method,
            url=path,
            params=params,
            json=json_data,
            headers=headers,
            **kwargs,
        )

        if response.status_code == 401:
            body = {}
            try:
                body = response.json()
            except:
                pass
            if body.get("code") == "GW.AUTHN":
                self.auth._access_token = None
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
        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    async def get(self, path: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return await self._request("GET", path, params=params, **kwargs)

    async def post(self, path: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return await self._request("POST", path, json_data=json_data, **kwargs)

    async def put(self, path: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return await self._request("PUT", path, json_data=json_data, **kwargs)

    async def patch(self, path: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return await self._request("PATCH", path, json_data=json_data, **kwargs)

    async def delete(self, path: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return await self._request("DELETE", path, params=params, **kwargs)
