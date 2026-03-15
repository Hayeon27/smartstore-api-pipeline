import asyncio
import os
import json
import logging
from dotenv import load_dotenv
from client import NaverCommerceClient
from datetime import datetime, timedelta

# 로깅 설정
logging.basicConfig(level=logging.INFO)
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.DEBUG)

load_dotenv()

async def debug_pipeline_apis():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    async with NaverCommerceClient(client_id, client_secret) as client:
        print("\n--- 1. Products Search Debug ---")
        # main.py에서 성공했던 방식
        res1 = await client.products.search_products({})
        print(f"Empty Data Count: {len(res1.get('contents', []))}")
        
        # extractor.py 방식 (page=0)
        res2 = await client.products.search_products({"page": 0, "size": 50})
        print(f"Page 0 Count: {len(res2.get('contents', []))}")

        print("\n--- 2. Inquiries Debug ---")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # 인코딩 문제 가능성 대비하여 +를 %2B로 명시해보기 (또는 그냥 시간만 전송)
        # Naver API는 'yyyy-MM-ddTHH:mm:ssZ' 또는 '+09:00' 형식을 받음
        customer_params = {
            "fromDate": start_date.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
            "toDate": end_date.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
            "page": 1,
            "size": 50
        }
        print(f"Sending Customer Params: {customer_params}")
        try:
            res3 = await client.inquiries.get_customer_inquiries(customer_params)
            print(f"Customer Inquiries Count: {len(res3.get('contents', []))}")
        except Exception as e:
            print(f"Customer Inquiry Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_pipeline_apis())
