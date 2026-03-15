"""기존 상품의 상태를 판매중지로 변경."""

import asyncio
import os
from dotenv import load_dotenv
from client import NaverCommerceClient

load_dotenv()

async def fix_product_status(product_no):
    async with NaverCommerceClient(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET")) as client:
        print(f"🚀 상품 {product_no}의 상태를 '판매중지(SUSPENSION)'로 변경합니다...")
        try:
            # PUT /v1/products/origin-products/{originProductNo}/change-status
            # status 값: SALE, OUT_OF_STOCK, SALE_END, SUSPENSION
            result = await client.products.change_product_status(product_no, "SUSPENSION")
            print(f"✅ 상태 변경 성공!")
            print(f"응답: {result}")
        except Exception as e:
            print(f"❌ 상태 변경 실패: {e}")

if __name__ == "__main__":
    # 방금 등록된 상품 번호 입력
    fix_product_status_no = "13196083419"
    asyncio.run(fix_product_status(fix_product_status_no))
    
    # 상태 재확인
    import subprocess
    subprocess.run(["uv", "run", "python", "check_status.py"])
