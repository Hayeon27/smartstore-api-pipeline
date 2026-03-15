"""데이터 수집 및 변환 모듈."""

import logging
from typing import List, Dict, Any, Optional
from client import NaverCommerceClient

logger = logging.getLogger(__name__)

class DataExtractor:
    """네이버 커머스 API로부터 데이터를 추출하는 엔진."""

    def __init__(self, client: NaverCommerceClient):
        self.client = client

    async def fetch_all_products(self) -> List[Dict[str, Any]]:
        """전체 상품 목록 수집 (v1/products/search 활용)."""
        logger.info("Fetching all products...")
        all_products = []
        page = 1
        size = 50
        
        while True:
            params = {
                "searchKeywordType": "SELLER_CODE",
                "page": page,
                "size": size
            }
            result = await self.client.products.search_products(params)
            contents = result.get("contents", [])
            if not contents:
                break
            
            all_products.extend(contents)
            logger.debug(f"Fetched page {page} with {len(contents)} products.")
            
            if len(contents) < size:
                break
            page += 1
            
        logger.info(f"Total products fetched: {len(all_products)}")
        return all_products

    async def fetch_recent_orders(self, days: int = 7) -> List[Dict[str, Any]]:
        """최근 주문 목록 수집 (v1/pay-order/seller/product-orders/query 활용)."""
        # 정밀한 날짜 필터링이 필요할 수 있으나, 여기서는 기본적인 조회를 수행
        logger.info(f"Fetching recent orders (last {days} days)...")
        # 실제 구현 시에는 API 문서에 맞게 날짜 파라미터를 구성해야 함
        # 현재 OrdersClient에는 query_product_orders가 있으므로 이를 활용
        
        # 임시 예시 파라미터 (실제 스펙에 맞춰 고도화 필요)
        all_orders = []
        # ... 주문 수집 로직 ...
        return all_orders

    async def fetch_all_inquiries(self) -> List[Dict[Dict[str, Any]]]:
        """고객 문의 및 상품 Q&A 수집."""
        logger.info("Fetching inquiries...")
        # 1. 고객 문의
        customer_inquiries = await self.client.inquiries.get_customer_inquiries({"page": 1, "size": 50})
        # 2. 상품 Q&A
        product_qnas = await self.client.inquiries.get_product_inquiries({"page": 1, "size": 50})
        
        # 통일된 포맷으로 변환 필요
        return {
            "customer": customer_inquiries.get("contents", []),
            "product": product_qnas.get("contents", [])
        }
