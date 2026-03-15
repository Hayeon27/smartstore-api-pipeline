"""네이버 커머스 API 상품(Products) 클라이언트."""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from client import NaverCommerceClient


class ProductsClient:
    """상품 정보 관련 API 클라이언트.
    
    공식 문서: https://apicenter.commerce.naver.com/docs/commerce-api/current/%EC%83%81%ED%92%88
    """

    def __init__(self, client: "NaverCommerceClient"):
        self.client = client

    # --- 브랜드 (Brand) ---
    async def get_brands(self, name: Optional[str] = None) -> List[Dict[str, Any]]:
        """브랜드 목록 조회.
        GET /v1/product-brands
        """
        params = {"name": name} if name else {}
        return await self.client.get("/v1/product-brands", params=params)

    # --- 사이즈 (Size) ---
    async def get_size_types(self) -> List[Dict[str, Any]]:
        """전체 사이즈 타입 조회.
        GET /v1/product-sizes
        """
        return await self.client.get("/v1/product-sizes")

    async def get_size_type(self, size_type_id: int) -> Dict[str, Any]:
        """특정 사이즈 타입 조회.
        GET /v1/product-sizes/{sizeTypeId}
        """
        return await self.client.get(f"/v1/product-sizes/{size_type_id}")

    # --- 상품 검수 (Product Inspection) ---
    async def restore_inspected_product(self, channel_product_no: str) -> Dict[str, Any]:
        """수정 요청 상품에 대해 복원 요청.
        PUT /v1/product-inspections/channel-product/{channelProductNo}/restore
        """
        return await self.client.put(f"/v1/product-inspections/channel-product/{channel_product_no}/restore")

    async def get_inspection_requests(self, page: int = 0, size: int = 20) -> Dict[str, Any]:
        """수정 요청 상품 목록 조회.
        GET /v1/product-inspections/requests
        """
        params = {"page": page, "size": size}
        return await self.client.get("/v1/product-inspections/requests", params=params)

    # --- 그룹상품 (Group Products) - v2 ---
    async def create_group_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """[v2] 그룹상품 등록.
        POST /v2/standard-group-products
        """
        return await self.client.post("/v2/standard-group-products", json_data=data)

    async def get_group_product_status(self, request_id: str) -> Dict[str, Any]:
        """[v2] 그룹상품 요청 결과 조회.
        GET /v2/standard-group-products/status
        """
        params = {"requestId": request_id}
        return await self.client.get("/v2/standard-group-products/status", params=params)

    async def save_temp_detail_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """[v2] 상품 상세 정보 임시 저장.
        POST /v2/standard-group-products/temp-detail-content
        """
        return await self.client.post("/v2/standard-group-products/temp-detail-content", json_data=data)

    async def get_group_product(self, group_product_no: str) -> Dict[str, Any]:
        """[v2] 그룹상품 조회.
        GET /v2/standard-group-products/{groupProductNo}
        """
        return await self.client.get(f"/v2/standard-group-products/{group_product_no}")

    async def update_group_product(self, group_product_no: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """[v2] 그룹상품 수정.
        PUT /v2/standard-group-products/{groupProductNo}
        """
        return await self.client.put(f"/v2/standard-group-products/{group_product_no}", json_data=data)

    async def delete_group_product(self, group_product_no: str) -> Dict[str, Any]:
        """[v2] 그룹상품 삭제.
        DELETE /v2/standard-group-products/{groupProductNo}
        """
        return await self.client.delete(f"/v2/standard-group-products/{group_product_no}")

    # --- 일반 상품 (General Products) ---
    async def update_multi_products(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """멀티 상품 변경.
        PATCH /v1/products/origin-products/multi-update
        """
        return await self.client.patch("/v1/products/origin-products/multi-update", json_data=data)

    async def change_product_status(self, origin_product_no: str, status: str) -> Dict[str, Any]:
        """판매 상태 변경.
        PUT /v1/products/origin-products/{originProductNo}/change-status
        """
        params = {"status": status}
        return await self.client.put(f"/v1/products/origin-products/{origin_product_no}/change-status", params=params)

    async def update_option_stock(self, origin_product_no: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """상품 옵션 재고 변경.
        PUT /v1/products/origin-products/{originProductNo}/option-stock
        """
        return await self.client.put(f"/v1/products/origin-products/{origin_product_no}/option-stock", json_data=data)

    async def create_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """[v2] 상품 등록.
        POST /v2/products
        """
        return await self.client.post("/v2/products", json_data=data)

    async def get_channel_product(self, channel_product_no: str) -> Dict[str, Any]:
        """[v2] 채널 상품 조회.
        GET /v2/products/channel-products/{channelProductNo}
        """
        return await self.client.get(f"/v2/products/channel-products/{channel_product_no}")

    async def update_channel_product(self, channel_product_no: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """[v2] 채널 상품 수정.
        PUT /v2/products/channel-products/{channelProductNo}
        """
        return await self.client.put(f"/v2/products/channel-products/{channel_product_no}", json_data=data)

    async def delete_channel_product(self, channel_product_no: str) -> Dict[str, Any]:
        """[v2] 채널 상품 삭제.
        DELETE /v2/products/channel-products/{channelProductNo}
        """
        return await self.client.delete(f"/v2/products/channel-products/{channel_product_no}")

    async def get_origin_product(self, origin_product_no: str) -> Dict[str, Any]:
        """[v2] 원상품 조회.
        GET /v2/products/origin-products/{originProductNo}
        """
        return await self.client.get(f"/v2/products/origin-products/{origin_product_no}")

    async def update_origin_product(self, origin_product_no: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """[v2] 원상품 수정.
        PUT /v2/products/origin-products/{originProductNo}
        """
        return await self.client.put(f"/v2/products/origin-products/{origin_product_no}", json_data=data)

    async def delete_origin_product(self, origin_product_no: str) -> Dict[str, Any]:
        """[v2] 원상품 삭제.
        DELETE /v2/products/origin-products/{originProductNo}
        """
        return await self.client.delete(f"/v2/products/origin-products/{origin_product_no}")

    # --- 상품 목록 (Product List) ---
    async def search_products(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """상품 목록 조회.
        POST /v1/products/search
        """
        # 필수 필드 searchKeywordType이 없을 경우 기본값 SELLER_CODE 설정 (목록 조회를 위해)
        if "searchKeywordType" not in data:
            data["searchKeywordType"] = "SELLER_CODE"
        return await self.client.post("/v1/products/search", json_data=data)
