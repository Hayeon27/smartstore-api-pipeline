"""데이터 수집 및 변환 모듈."""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
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
        page = 0
        size = 50
        
        while True:
            params = {"page": page, "size": size}
            result = await self.client.products.search_products(params)
            contents = result.get("contents", [])
            if not contents:
                break
            
            all_products.extend(contents)
            logger.info(f"Fetched page {page} with {len(contents)} products.")
            
            if len(contents) < size:
                break
            page += 1
            
        return all_products

    async def fetch_all_inquiries(self, days: int = 30) -> Dict[str, Any]:
        """고객 문의 및 상품 Q&A 수집."""
        logger.info(f"Fetching inquiries (last {days} days)...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 날짜 포맷팅 (YYYY-MM-DDTHH:mm:ss 형식으로 시도)
        start_str = start_date.strftime("%Y-%m-%dT%H:%M:%S")
        end_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")
        
        logger.info(f"Using date range: {start_str} to {end_str}")

        # 1. 고객 문의 (GET /v1/pay-user/inquiries)
        customer_params = {
            "fromDate": start_str,
            "toDate": end_str,
            "page": 1,
            "size": 50
        }
        
        # 2. 상품 Q&A (GET /v1/contents/qnas)
        qna_params = {
            "startSearchDate": start_str,
            "endSearchDate": end_str,
            "page": 1,
            "size": 50
        }
        
        customer_list = []
        try:
            res = await self.client.inquiries.get_customer_inquiries(customer_params)
            customer_list = res.get("contents", [])
            logger.info(f"Fetched {len(customer_list)} customer inquiries.")
        except Exception as e:
            logger.warning(f"Failed to fetch customer inquiries: {e}")

        product_list = []
        try:
            res = await self.client.inquiries.get_product_inquiries(qna_params)
            product_list = res.get("contents", [])
            logger.info(f"Fetched {len(product_list)} product Q&As.")
        except Exception as e:
            logger.warning(f"Failed to fetch product Q&As: {e}")

        return {"customer": customer_list, "product": product_list}
