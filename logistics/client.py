"""네이버 커머스 API 물류(Logistics) 클라이언트."""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from client import NaverCommerceClient


class LogisticsClient:
    """물류 및 SKU 관련 API 클라이언트.
    
    공식 문서: https://apicenter.commerce.naver.com/docs/commerce-api/current/%EB%AC%BC%EB%A5%98
    """

    def __init__(self, client: "NaverCommerceClient"):
        self.client = client

    async def get_skus(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """SKU 목록 조회.
        POST /v1/logistics/products/sellers/me/skus/query-paged-list
        """
        return await self.client.post("/v1/logistics/products/sellers/me/skus/query-paged-list", json_data=data)

    async def get_sku(self, ns_id: str) -> Dict[str, Any]:
        """SKU 상세 조회.
        GET /v1/logistics/products/sellers/me/skus/{nsId}
        """
        return await self.client.get(f"/v1/logistics/products/sellers/me/skus/{ns_id}")

    async def get_sku_linked_products(self, ns_id: str) -> List[Dict[str, Any]]:
        """SKU 연결상품 조회.
        GET /v1/logistics/products/sellers/me/skus/{nsId}/product-mappings
        """
        return await self.client.get(f"/v1/logistics/products/sellers/me/skus/{ns_id}/product-mappings")
