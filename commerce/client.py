"""네이버 커머스 API 커머스 솔루션(Commerce Solutions) 클라이언트."""

from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from client import NaverCommerceClient


class CommerceSolutionClient:
    """커머스 솔루션 구독 관리 관련 API 클라이언트.
    
    공식 문서: https://apicenter.commerce.naver.com/docs/commerce-api/current/%EC%BB%A4%EB%A8%B8%EC%8A%A4%EC%86%94%EB%A3%A8%EC%85%98
    """

    def __init__(self, client: "NaverCommerceClient"):
        self.client = client

    async def approve_subscription(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """사용 시작 승인.
        PUT /v1/commerce-solutions/subscriptions/approve
        """
        return await self.client.put("/v1/commerce-solutions/subscriptions/approve", json_data=data)

    async def terminate_subscription(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """사용 해지 승인.
        PUT /v1/commerce-solutions/subscriptions/terminate
        """
        return await self.client.put("/v1/commerce-solutions/subscriptions/terminate", json_data=data)

    async def get_subscriptions(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """사용 상태 조회.
        GET /v1/commerce-solutions/subscriptions
        """
        return await self.client.get("/v1/commerce-solutions/subscriptions", params=params)

    async def reject_subscription(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """사용 시작 거절.
        PUT /v1/commerce-solutions/subscriptions/reject
        """
        return await self.client.put("/v1/commerce-solutions/subscriptions/reject", json_data=data)
