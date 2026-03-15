"""상품 관리 상태 변경 (v2 업데이트 API 활용)."""

import asyncio
import os
import json
from dotenv import load_dotenv
from client import NaverCommerceClient

load_dotenv()

async def update_product_to_suspended(product_no):
    async with NaverCommerceClient(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET")) as client:
        print(f"🔍 상품 {product_no}의 최신 정보를 가져옵니다...")
        # 1. 현재 정보 조회
        current = await client.products.get_origin_product(product_no)
        
        # 2. 상태값 변경 (SALE -> SUSPENSION)
        # originProduct와 smartstoreChannelProduct가 포함된 구조로 전송해야 함
        origin_data = current.get("originProduct")
        channel_data = current.get("smartstoreChannelProduct")
        
        if not origin_data:
            print("❌ 상품 정보를 불러올 수 없습니다.")
            return
            
        origin_data["statusType"] = "SUSPENSION"
        # channel_data는 이미 SUSPENSION일 수 있지만 확실히 보장
        if channel_data:
            channel_data["channelProductDisplayStatusType"] = "SUSPENSION"
        
        update_data = {
            "originProduct": origin_data,
            "smartstoreChannelProduct": channel_data
        }
        
        print(f"🚀 상품 {product_no}의 상태를 v2 API로 업데이트 중...")
        try:
            # PUT /v2/products/origin-products/{originProductNo}
            result = await client.products.update_origin_product(product_no, update_data)
            print(f"✅ 업데이트 성공!")
            # print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"❌ 업데이트 실패: {e}")

if __name__ == "__main__":
    target_no = "13196083419"
    asyncio.run(update_product_to_suspended(target_no))
    
    # 결과 확인
    import subprocess
    subprocess.run(["uv", "run", "python", "check_status.py"])
