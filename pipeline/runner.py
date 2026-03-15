"""파이프라인 실행 메인 모듈."""

import asyncio
import logging
import os
from dotenv import load_dotenv
from client import NaverCommerceClient
from .extractor import DataExtractor
from .storage import StorageManager
from .notifier import Notifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

class PipelineRunner:
    """ETL 파이프라인 실행 관리자."""

    def __init__(self, client: NaverCommerceClient = None):
        """
        client가 제공되면 해당 클라이언트를 사용하고,
        없으면 직접 .env 설정을 읽어 생성합니다.
        """
        load_dotenv()
        self.internal_client = client
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.storage = StorageManager()
        self.notifier = Notifier()

    async def run(self):
        """전체 파이프라인 프로세스 실행."""
        if self.internal_client:
            await self._execute(self.internal_client)
        else:
            if not self.client_id or not self.client_secret:
                logger.error("CLIENT_ID or CLIENT_SECRET is missing in .env")
                return
            async with NaverCommerceClient(self.client_id, self.client_secret) as client:
                await self._execute(client)

    async def _execute(self, client: NaverCommerceClient):
        """실제 수집 및 저장 로직."""
        extractor = DataExtractor(client)
        
        logger.info("=== Starting Data Pipeline ===")
        
        # 1. Products Extraction & Load
        try:
            products = await extractor.fetch_all_products()
            self.storage.upsert_products(products)
            
            # 신규 상품 알림 (예시: 이번 회차에 수집된 건 알림)
            if products:
                await self.notifier.notify_new_products(products)
        except Exception as e:
            logger.error(f"Failed to process products: {e}")

        # 2. Inquiries Extraction & Load
        try:
            inquiries_data = await extractor.fetch_all_inquiries()
            # 고객 문의 + 상품 Q&A 통합 저장
            all_inqs = inquiries_data.get("customer", []) + inquiries_data.get("product", [])
            self.storage.upsert_inquiries(all_inqs)
            
            # 알림 발송
            if all_inqs:
                await self.notifier.notify_new_inquiries(inquiries_data)
        except Exception as e:
            logger.error(f"Failed to process inquiries: {e}")

        # 3. Orders (추후 확장 가능)
        # TODO: orders 에 대한 Fetch & Load & Notify 추가 가능

        logger.info("=== Pipeline Execution Finished ===")

if __name__ == "__main__":
    runner = PipelineRunner()
    asyncio.run(runner.run())
