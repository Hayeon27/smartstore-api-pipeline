"""실제 상품 모사 등록 및 파이프라인 동기화 테스트 (최종 보정 버전)."""

import asyncio
import os
import logging
import sqlite3
from dotenv import load_dotenv
from client import NaverCommerceClient
from pipeline.runner import PipelineRunner

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

async def run_copy_test():
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    async with NaverCommerceClient(client_id, client_secret) as client:
        # STEP 1: 실제 상품 정보를 바탕으로 등록 데이터 구성
        # 성공이 검증된 demo_e2e.py의 구조를 100% 활용
        product_name = "남자 윈저 신사 정장 양말 (Copy Demo)"
        print(f"\n--- STEP 1: 실제 상품 모사 등록 시도 ({product_name}) ---")
        
        addr_res = await client.seller.get_address_books()
        addr_id = addr_res.get("addressBooks", [{}])[0].get("addressBookNo")
        
        product_data = {
            "originProduct": {
                "statusType": "SUSPENSION",
                "saleType": "NEW",
                "leafCategoryId": "50004002",
                "name": product_name,
                "detailContent": "<p>필로이 남자 윈저 신사 정장 양말 모사 최종 테스트 상품입니다.</p>",
                "images": {"representativeImage": {"url": "https://shop-phinf.pstatic.net/20250429_98/1745894309931DFWtl_JPEG/8879163620611368_1133996340.jpg"}},
                "salePrice": 3500, # 실제 가격 반영
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
                    "afterServiceInfo": {"afterServiceTelephoneNumber": "01012345678", "afterServiceGuideContent": "문의바람"},
                    "originAreaInfo": {"originAreaCode": "00", "content": "국산", "plural": False},
                    "taxType": "TAX", "minorPurchasable": True,
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
            "smartstoreChannelProduct": {"naverShoppingRegistration": False, "channelProductDisplayStatusType": "SUSPENSION"}
        }
        
        try:
            reg_res = await client.products.create_product(product_data)
            origin_no = reg_res.get("originProductNo")
            print(f"✅ 상품 모사 등록 성공! 원상품번호: {origin_no}")
            
            print(f"⌛ 인덱싱을 위해 10초간 대기합니다...")
            await asyncio.sleep(10)
            
            # STEP 2: 파이프라인 실행
            print(f"\n--- STEP 2: 파이프라인 실행 ---")
            runner = PipelineRunner(client)
            await runner.run()

            # STEP 3: DB 적재 확인
            print(f"\n--- STEP 3: 로컬 DB 적재 확인 ---")
            conn = sqlite3.connect("data/smartstore.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name, sale_price FROM products WHERE origin_product_no = ?", (origin_no,))
            row = cursor.fetchone()
            if row:
                print(f"✅ DB 확인 완료: 상품명='{row[0]}', 가격={row[1]}")
            else:
                print(f"❌ DB에서 해당 상품({origin_no})을 찾을 수 없습니다.")
            conn.close()

        except Exception as e:
            print(f"❌ 작업 중 오류 발생:\n{e}")

if __name__ == "__main__":
    asyncio.run(run_copy_test())
