"""전체 파이프라인 통합 데모 (E2E)."""

import asyncio
import os
import logging
from dotenv import load_dotenv
from client import NaverCommerceClient
from pipeline.runner import PipelineRunner
import sqlite3

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

async def run_demo():
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    async with NaverCommerceClient(client_id, client_secret) as client:
        # STEP 1: 신규 테스트 상품 등록 (안전 모드: SUSPENSION)
        product_name = f"데모 상품_안전_{os.urandom(2).hex()}"
        print(f"\n--- STEP 1: 신규 상품 등록 시도 ({product_name}) ---")
        
        # 주소록 조회
        addr_res = await client.seller.get_address_books()
        addr_id = addr_res.get("addressBooks", [{}])[0].get("addressBookNo")
        
        product_data = {
            "originProduct": {
                "statusType": "SUSPENSION", # 판매 x
                "saleType": "NEW",
                "leafCategoryId": "50004002",
                "name": product_name,
                "detailContent": "<p>E2E 파이프라인 통합 데모 상품입니다.</p>",
                "images": {"representativeImage": {"url": "https://shop-phinf.pstatic.net/20260315_125/1773576259685fOWHl_JPEG/107709135808871641_123963431.jpg"}},
                "salePrice": 10000,
                "stockQuantity": 100,
                "deliveryInfo": {
                    "deliveryType": "DELIVERY",
                    "deliveryAttributeType": "NORMAL",
                    "deliveryCompany": "CJGLS",
                    "deliveryFee": {"deliveryFeeType": "FREE"},
                    "claimDeliveryInfo": {
                        "returnDeliveryCompanyPriorityType": "PRIMARY",
                        "returnDeliveryFee": 3000, "exchangeDeliveryFee": 6000,
                        "shippingAddressId": addr_id, "returnAddressId": addr_id, "freeReturnInsuranceYn": False
                    }
                },
                "detailAttribute": {
                    "afterServiceInfo": {
                        "afterServiceTelephoneNumber": "01012345678",
                        "afterServiceGuideContent": "문의는 010-1234-5678로 연락 바랍니다."
                    },
                    "originAreaInfo": {
                        "originAreaCode": "00",
                        "content": "국산",
                        "plural": False
                    },
                    "taxType": "TAX",
                    "minorPurchasable": True,
                    "productInfoProvidedNotice": {
                        "productInfoProvidedNoticeType": "FASHION_ITEMS",
                        "fashionItems": {
                            "type": "양말",
                            "material": "면",
                            "size": "Free",
                            "manufacturer": "한국",
                            "caution": "test",
                            "warrantyPolicy": "test",
                            "afterServiceDirector": "01012345678"
                        }
                    }
                }
            },
            "smartstoreChannelProduct": {"naverShoppingRegistration": False, "channelProductDisplayStatusType": "SUSPENSION"} # 전시 x
        }
        
        try:
            reg_res = await client.products.create_product(product_data)
            origin_no = reg_res.get("originProductNo")
            print(f"✅ 상품 등록 성공! 원상품번호: {origin_no}")
            
            print(f"⌛ 인덱싱을 위해 5초간 대기합니다...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"❌ 상품 등록 실패 (중단): {e}")
            return

        # STEP 2: 파이프라인 (ETL) 실행
        print(f"\n--- STEP 2: 파이프라인 실행 ---")
        runner = PipelineRunner(client)
        await runner.run()

        # STEP 3: DB 적재 확인
        print(f"\n--- STEP 3: 로컬 DB 적재 확인 ---")
        conn = sqlite3.connect("data/smartstore.db")
        cursor = conn.cursor()
        
        # 전체 상품 수 확인
        cursor.execute("SELECT COUNT(*) FROM products")
        total_count = cursor.fetchone()[0]
        print(f"📊 현재 DB 내 전체 상품 수: {total_count}")

        # 방금 등록한 상품 확인
        cursor.execute("SELECT name, sale_price FROM products WHERE origin_product_no = ?", (origin_no,))
        row = cursor.fetchone()
        if row:
            print(f"✅ DB 확인 완료: 상품명='{row[0]}', 가격={row[1]}")
        else:
            print(f"❌ DB에서 해당 상품({origin_no})을 찾을 수 없습니다.")
        conn.close()

        print(f"\n--- 데모 완료 ---")

if __name__ == "__main__":
    asyncio.run(run_demo())
