"""네이버 커머스API 인증 토큰 발급 모듈.

공식 문서: https://apicenter.commerce.naver.com/docs/auth
- OAuth2 Client Credentials Grant
- bcrypt 전자서명 + Base64 인코딩
- POST /v1/oauth2/token
- 토큰 유효시간: 3시간 (10,800초)
"""

import time
import logging

import bcrypt
import pybase64
import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://api.commerce.naver.com/external"


def generate_signature(client_id: str, client_secret: str, timestamp: int) -> str:
    """bcrypt 전자서명 생성 후 Base64 인코딩.

    공식 문서 알고리즘:
    1. password = "{client_id}_{timestamp}"
    2. salt = client_secret
    3. bcrypt.hashpw(password, salt)
    4. base64 standard encode

    Args:
        client_id: 애플리케이션 ID.
        client_secret: 애플리케이션 시크릿 (bcrypt salt 형식).
        timestamp: 밀리초 단위 Unix 시간.

    Returns:
        Base64 인코딩된 전자서명 문자열.
    """
    password = f"{client_id}_{timestamp}"
    hashed = bcrypt.hashpw(password.encode("utf-8"), client_secret.encode("utf-8"))
    return pybase64.standard_b64encode(hashed).decode("utf-8")


class NaverAuth:
    """네이버 커머스API 인증 토큰 관리.

    토큰 발급, 캐싱, 자동 갱신을 처리합니다.
    """

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self._access_token: str | None = None
        self._expires_at: float = 0  # Unix timestamp (seconds)

    @property
    def is_token_valid(self) -> bool:
        """토큰이 유효한지 확인 (만료 30분 전부터 갱신 대상)."""
        if not self._access_token:
            return False
        return time.time() < (self._expires_at - 1800)  # 30분 여유

    async def get_token(self) -> str:
        """유효한 인증 토큰 반환. 만료 시 자동 갱신.

        Returns:
            Bearer 토큰 문자열.
        """
        if self.is_token_valid:
            return self._access_token

        await self._request_token()
        return self._access_token

    async def _request_token(self) -> None:
        """POST /v1/oauth2/token 으로 토큰 발급 요청."""
        timestamp = int(time.time() * 1000)
        signature = generate_signature(self.client_id, self.client_secret, timestamp)

        url = f"{BASE_URL}/v1/oauth2/token"
        params = {
            "client_id": self.client_id,
            "timestamp": timestamp,
            "client_secret_sign": signature,
            "grant_type": "client_credentials",
            "type": "SELF",
        }

        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(url, data=params)

        if response.status_code != 200:
            logger.error(
                "토큰 발급 실패: status=%d, body=%s",
                response.status_code,
                response.text,
            )
            from exceptions import AuthenticationError

            body = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
            raise AuthenticationError(
                status_code=response.status_code,
                code=body.get("code", "UNKNOWN"),
                message=body.get("message", response.text),
                trace_id=body.get("traceId", ""),
            )

        data = response.json()
        self._access_token = data["access_token"]
        # expires_in은 초 단위
        expires_in = data.get("expires_in", 10800)
        self._expires_at = time.time() + expires_in

        logger.info("토큰 발급 성공 (expires_in=%d초)", expires_in)
