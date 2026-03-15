"""네이버 커머스 API 판매자(Seller) 클라이언트."""

from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from client import NaverCommerceClient


class SellerClient:
    """판매자 정보 관련 API 클라이언트.
    
    공식 문서: https://apicenter.commerce.naver.com/docs/commerce-api/current/%ED%8C%90%EB%A7%A4%EC%9E%90
    """

    def __init__(self, client: "NaverCommerceClient"):
        self.client = client

    async def get_account(self) -> Dict[str, Any]:
        """계정 정보 조회.
        
        조회 대상 판매자 번호에 대한 인증 토큰이 필요합니다.
        GET /v1/seller/account
        """
        return await self.client.get("/v1/seller/account")

    async def get_channels(self) -> List[Dict[str, Any]]:
        """계정 하위의 채널 정보 조회.
        GET /v1/seller/channels
        """
        return await self.client.get("/v1/seller/channels")

    async def get_seller_info_by_token(self) -> Dict[str, Any]:
        """판매자 인증 JWE 해석.
        GET /v1/commerce-solutions/seller-info-by-token
        """
        # 참고: 경로는 commerce-solutions 아래에 있으나 판매자 정보 범주로 분류됨
        return await self.client.get("/v1/commerce-solutions/seller-info-by-token")
