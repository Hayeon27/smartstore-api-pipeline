"""네이버 커머스 API 정산(Settlement) 클라이언트."""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from client import NaverCommerceClient


class SettlementClient:
    """정산 및 부가세 관련 API 클라이언트.
    
    공식 문서: https://apicenter.commerce.naver.com/docs/commerce-api/current/%EC%A4%91%EC%82%B0
    """

    def __init__(self, client: "NaverCommerceClient"):
        self.client = client

    # --- 부가세 내역 (VAT Details) ---
    async def get_vat_case(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """건별 부가세 내역 조회.
        GET /v1/pay-settle/vat/case
        """
        return await self.client.get("/v1/pay-settle/vat/case", params=params)

    async def get_vat_daily(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """일별 부가세 내역 조회.
        GET /v1/pay-settle/vat/daily
        """
        return await self.client.get("/v1/pay-settle/vat/daily", params=params)

    # --- 정산 내역 (Settlement Details) ---
    async def get_settle_case(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """건별 정산 내역 조회.
        GET /v1/pay-settle/settle/case
        """
        return await self.client.get("/v1/pay-settle/settle/case", params=params)

    async def get_commission_details(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """수수료 상세 내역 조회.
        GET /v1/pay-settle/settle/commission-details
        """
        return await self.client.get("/v1/pay-settle/settle/commission-details", params=params)

    async def get_settle_daily(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """일별 정산 내역 조회.
        GET /v1/pay-settle/settle/daily
        """
        return await self.client.get("/v1/pay-settle/settle/daily", params=params)
