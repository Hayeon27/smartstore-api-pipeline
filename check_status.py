import asyncio
import os
import json
from dotenv import load_dotenv
from client import NaverCommerceClient

load_dotenv()

async def check_product_status(product_no):
    async with NaverCommerceClient(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET")) as client:
        print(f"🔍 상품 {product_no} 상세 상태 조회 중...")
        # 원상품 조회 (v2)
        origin = await client.products.get_origin_product(product_no)
        print(f"--- Origin Product Raw ---")
        print(json.dumps(origin, indent=2, ensure_ascii=False))
        # print(f"statusType: {origin.get('statusType')}")
        
        # 채널 상품 조회 (v2)
        # 원상품번호로 채널상품 목록을 가져와야 하는데, get_channel_product는 채널상품번호가 필요함.
        # 일단 search_products로 확인
        res = await client.products.search_products({"page":0, "size":10})
        for p in res.get("contents", []):
            if str(p.get("originProductNo")) == str(product_no):
                print(f"\n--- Search Result ---")
                channels = p.get("channelProducts", [])
                if channels:
                    print(f"channelProductNo: {channels[0].get('channelProductNo')}")
                    print(f"statusType: {channels[0].get('statusType')}") # 검색 결과에서의 statusType
                    # 채널별 상세 조회
                    ch_detail = await client.products.get_channel_product(channels[0].get('channelProductNo'))
                    print(f"channelProductDisplayStatusType: {ch_detail.get('channelProductDisplayStatusType')}")

if __name__ == "__main__":
    asyncio.run(check_product_status("13196083419"))
