"""파이프라인 실행 메인 모듈."""

import asyncio
import logging
import os
from dotenv import load_dotenv
from client import NaverCommerceClient
from .extractor import DataExtractor
from .storage import StorageManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

class PipelineRunner:
    """ETL 파이프라인 실행 관리자."""

    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.storage = StorageManager()

    async def run(self):
        """전체 파이프라인 프로세스 실행."""
        if not self.client_id or not self.client_secret:
            logger.error("CLIENT_ID or CLIENT_SECRET is missing in .env")
            return

        async with NaverCommerceClient(self.client_id, self.client_secret) as client:
            extractor = DataExtractor(client)
            
            logger.info("=== Starting Data Pipeline ===")
            
            # 1. Products Extraction & Load
            try:
                products = await extractor.fetch_all_products()
                self.storage.upsert_products(products)
            except Exception as e:
                logger.error(f"Failed to process products: {e}")

            # 2. Orders Extraction & Load (Placeholder)
            # orders = await extractor.fetch_recent_orders()
            # self.storage.upsert_orders(orders)

            # 3. Inquiries Extraction & Load
            try:
                inquiries_data = await extractor.fetch_all_inquiries()
                # 합쳐서 저장하거나 각각 저장 (현재 storage는 inquiries 하나로 되어 있음)
                # 여기서는 간단히 product_qna를 위주로 시연
                self.storage.upsert_inquiries(inquiries_data["product"])
            except Exception as e:
                logger.error(f"Failed to process inquiries: {e}")

            logger.info("=== Pipeline Execution Finished ===")

if __name__ == "__main__":
    runner = PipelineRunner()
    asyncio.run(runner.run())
