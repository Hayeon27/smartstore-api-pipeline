"""데이터 수집 및 변환 모듈."""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from client import NaverCommerceClient

logger = logging.getLogger(__name__)

class DataExtractor:
    """네이버 스마트스토어 API에서 데이터를 추출하는 엔진."""

    def __init__(self, client: NaverCommerceClient):
        self.client = client

    async def fetch_all_products(self) -> List[Dict[str, Any]]:
        """전체 상품 목록 수집."""
        logger.info("Fetching all products...")
        all_products = []
        page = 0
        size = 50
        
        while True:
            params = {
                "page": page,
                "size": size
            }
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
        
        # 날짜 포맷팅 (YYYY-MM-DDTHH:mm:ss.000Z 형식 - 공식 명세 준수)
        # Naver API v2는 밀리초와 Z(UTC) 접미사를 요구하는 경우가 많음
        start_str = start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        end_str = end_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
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
            "fromDate": start_str,
            "toDate": end_str,
            "page": 1,
            "size": 50
        }

        results = {"customer": [], "product": []}

        try:
            # 고객 문의 요청
            cust_res = await self.client.inquiries.get_customer_inquiries(customer_params)
            results["customer"] = cust_res.get("contents", [])
            logger.info(f"Fetched {len(results['customer'])} customer inquiries.")
        except Exception as e:
            logger.error(f"Failed to fetch customer inquiries: {e}")

        try:
            # 상품 Q&A 요청
            prod_res = await self.client.inquiries.get_product_inquiries(qna_params)
            results["product"] = prod_res.get("contents", [])
            logger.info(f"Fetched {len(results['product'])} product Q&As.")
        except Exception as e:
            logger.error(f"Failed to fetch product Q&As: {e}")

        return results

    async def fetch_daily_stats(self, days: int = 7) -> List[Dict[str, Any]]:
        """최근 N일간의 일별 통계 데이터 수집."""
        logger.info(f"Fetching daily stats (last {days} days)...")
        stats_list = []
        
        for i in range(1, days + 1): # 어제부터 과거 N일까지
            date_str = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            try:
                res = await self.client.stats.get_all_channel_daily_report(params={"searchDate": date_str})
                # 응답 구조 예시: {"searchDate": "2024-03-14", "payAmt": 1000, "payCnt": 5, "visitCnt": 100}
                if res:
                    stats_list.append(res)
                    logger.debug(f"Fetched stats for {date_str}")
            except Exception as e:
                 logger.error(f"Failed to fetch stats for {date_str}: {e}")
        
        return stats_list

    async def fetch_recent_orders(self, days: int = 7) -> List[Dict[str, Any]]:
        """최근 N일간 상태가 변경된 주문 수집."""
        logger.info(f"Fetching recent order status changes (last {days} days)...")
        
        # Naver API: last-changed-status-datetime 기준으로 조회
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        start_str = start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
        params = {
            "lastChangedStatusDatetime": start_str,
            # "moreSequence": "" # 필요시 시퀀스 토큰 사용
        }
        
        try:
            res = await self.client.orders.get_changed_product_orders(params)
            data = res.get("data", {})
            last_changed_statuses = data.get("lastChangedStatuses", [])
            
            if not last_changed_statuses:
                logger.info("No recent order status changes found.")
                return []
            
            # 상품 주문 번호들만 추출
            p_order_ids = [item.get("productOrderId") for item in last_changed_statuses]
            logger.info(f"Found {len(p_order_ids)} changed product orders. Fetching details...")
            
            # 상세 정보 일괄 조회 (query_product_orders)
            # 최대 100건씩 끊어서 요청 (API 제한 대응)
            detailed_orders = []
            chunk_size = 100
            for i in range(0, len(p_order_ids), chunk_size):
                chunk = p_order_ids[i:i + chunk_size]
                details = await self.client.orders.query_product_orders(chunk)
                detailed_orders.extend(details)
            
            return detailed_orders
            
        except Exception as e:
            logger.error(f"Failed to fetch recent orders: {e}")
            return []
