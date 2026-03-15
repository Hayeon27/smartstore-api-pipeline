"""네이버 커머스 API 문의(Inquiries) 클라이언트."""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from client import NaverCommerceClient


class InquiriesClient:
    """고객 및 상품 문의 관련 API 클라이언트.
    
    공식 문서: https://apicenter.commerce.naver.com/docs/commerce-api/current/%EB%AC%B8%EC%9D%98
    """

    def __init__(self, client: "NaverCommerceClient"):
        self.client = client

    # --- 고객 문의 (Customer Inquiries) ---
    async def get_customer_inquiries(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """고객 문의 조회.
        GET /v1/pay-user/inquiries
        """
        return await self.client.get("/v1/pay-user/inquiries", params=params)

    async def register_customer_answer(self, inquiry_no: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """고객 문의 답변 등록.
        POST /v1/pay-merchant/inquiries/{inquiryNo}/answer
        """
        return await self.client.post(f"/v1/pay-merchant/inquiries/{inquiry_no}/answer", json_data=data)

    async def update_customer_answer(self, inquiry_no: str, answer_content_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """고객 문의 답변 수정.
        PUT /v1/pay-merchant/inquiries/{inquiryNo}/answer/{answerContentId}
        """
        return await self.client.put(f"/v1/pay-merchant/inquiries/{inquiry_no}/answer/{answer_content_id}", json_data=data)

    # --- 상품 문의 (Product Inquiries) ---
    async def get_product_inquiries(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """상품 문의 목록 조회.
        GET /v1/contents/qnas
        """
        return await self.client.get("/v1/contents/qnas", params=params)

    async def get_product_answer_templates(self) -> List[Dict[str, Any]]:
        """상품 문의 답변 템플릿 목록 조회.
        GET /v1/contents/qnas/templates
        """
        return await self.client.get("/v1/contents/qnas/templates")

    async def update_product_answer(self, qna_no: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """상품 문의 답변 등록/수정.
        PUT /v1/contents/qnas/{qnaNo}/answer
        """
        return await self.client.put(f"/v1/contents/qnas/{qna_no}/answer", json_data=data)
