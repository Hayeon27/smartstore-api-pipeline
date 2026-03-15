"""네이버 커머스 API 주문(Orders) 클라이언트."""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from client import NaverCommerceClient


class OrdersClient:
    """주문 및 풀필먼트 관련 API 클라이언트.
    
    공식 문서: https://apicenter.commerce.naver.com/docs/commerce-api/current/%EC%A3%BC%EB%AC%B8
    """

    def __init__(self, client: "NaverCommerceClient"):
        self.client = client

    async def get_product_order_ids(self, order_id: str) -> List[str]:
        """상품 주문 목록 조회.
        특정 주문 번호(orderId)에 포함된 상품 주문 번호 목록을 조회합니다.
        GET /v1/pay-order/seller/orders/{orderId}/product-order-ids
        """
        return await self.client.get(f"/v1/pay-order/seller/orders/{order_id}/product-order-ids")

    async def query_product_orders(self, product_order_ids: List[str]) -> List[Dict[str, Any]]:
        """상품 주문 상세 내역 조회.
        상품 주문 번호를 기반으로 주문의 상세 내역을 조회합니다.
        POST /v1/pay-order/seller/product-orders/query
        """
        data = {"productOrderIds": product_order_ids}
        return await self.client.post("/v1/pay-order/seller/product-orders/query", json_data=data)

    async def confirm_order(self, product_order_ids: List[str]) -> Dict[str, Any]:
        """발주 확인 처리.
        결제 완료된 상품 주문에 대해 발주 확인 처리를 수행합니다.
        POST /v1/pay-order/seller/product-orders/confirm
        """
        data = {"productOrderIds": product_order_ids}
        return await self.client.post("/v1/pay-order/seller/product-orders/confirm", json_data=data)

    async def dispatch_order(self, dispatch_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """발송 처리.
        송장 정보를 입력하고 실제 배송 처리를 시작합니다.
        POST /v1/pay-order/seller/product-orders/dispatch
        """
        data = {"dispatchProductOrders": dispatch_list}
        return await self.client.post("/v1/pay-order/seller/product-orders/dispatch", json_data=data)

    async def delay_dispatch(self, delay_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """발송 지연 처리.
        발송 지연 사유와 예정일을 등록합니다.
        POST /v1/pay-order/seller/product-orders/delay-dispatch
        """
        data = {"delayDispatchProductOrders": delay_list}
        return await self.client.post("/v1/pay-order/seller/product-orders/delay-dispatch", json_data=data)

    async def get_changed_product_orders(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """최근 상태가 변경된 상품 주문 목록 조회.
        GET /v1/pay-order/seller/product-orders/last-changed-status
        """
        return await self.client.get("/v1/pay-order/seller/product-orders/last-changed-status", params=params)
