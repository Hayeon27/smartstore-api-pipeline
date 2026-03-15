"""상품 등록(v2) 샘플 스크립트 (최종 보정 버전)."""

import asyncio
import os
import json
from dotenv import load_dotenv
from client import NaverCommerceClient

load_dotenv()

async def register_sample_product():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    async with NaverCommerceClient(client_id, client_secret) as client:
        # 1. 주소록 정보 조회 및 출고지/반품지 자동 매핑
        print("🔍 주소록 정보를 조회하여 출고지 및 반품지 ID를 확인합니다...")
        address_books_res = await client.seller.get_address_books()
        address_books = address_books_res.get("addressBooks", [])
        
        release_id = None
        refund_id = None
        
        for addr in address_books:
            if addr.get("addressType") == "RELEASE" and not release_id:
                release_id = addr.get("addressBookNo")
            if addr.get("addressType") == "REFUND_OR_EXCHANGE" and not refund_id:
                refund_id = addr.get("addressBookNo")
        
        # 만약 하나만 있다면 둘 다 같은 ID로 대체 사용 (최소한의 가동 보장)
        if not release_id and address_books: release_id = address_books[0].get("addressBookNo")
        if not refund_id and address_books: refund_id = address_books[0].get("addressBookNo")
        
        if not release_id or not refund_id:
            print("⚠️ 유효한 주소록이 없습니다. 스마트스토어 센터에서 주소지를 먼저 등록해주세요.")
            return

        print(f"👉 출고지ID: {release_id} | 반품지ID: {refund_id}")

        # 2. 상품 등록 데이터 준비 (성공 사례인 product_debug.json 구조 완벽 반영)
        product_data = {
            "originProduct": {
                "statusType": "SALE",
                "saleType": "NEW",
                "leafCategoryId": "50004002", # 양말 카테고리
                "name": "API 테스트 등록 상품 (최종형)",
                "detailContent": "<div class=\"se-viewer se-theme-default\" lang=\"ko-KR\"><div class=\"se-main-container\"><p>API를 통한 자동 등록 테스트입니다.</p></div></div>",
                "images": {
                    "representativeImage": {
                        "url": "https://shop-phinf.pstatic.net/20260315_125/1773576259685fOWHl_JPEG/107709135808871641_123963431.jpg"
                    }
                },
                "salePrice": 12500,
                "stockQuantity": 1000,
                "deliveryInfo": {
                    "deliveryType": "DELIVERY",
                    "deliveryAttributeType": "NORMAL",
                    "deliveryCompany": "CJGLS",
                    "deliveryBundleGroupUsable": True,
                    "deliveryFee": {
                        "deliveryFeeType": "FREE",
                        "baseFee": 0
                    },
                    "claimDeliveryInfo": {
                        "returnDeliveryCompanyPriorityType": "PRIMARY",
                        "returnDeliveryFee": 3000,
                        "exchangeDeliveryFee": 6000,
                        "shippingAddressId": release_id,
                        "returnAddressId": refund_id,
                        "freeReturnInsuranceYn": False
                    }
                },
                "detailAttribute": {
                    "afterServiceInfo": {
                        "afterServiceTelephoneNumber": "01012345678",
                        "afterServiceGuideContent": "문의는 010-1234-5678로 연락 바랍니다."
                    },
                    "originAreaInfo": {
                        "originAreaCode": "00", # 국산
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
            "smartstoreChannelProduct": {
                "naverShoppingRegistration": True,
                "channelProductDisplayStatusType": "ON"
            }
        }

        # 3. 상품 등록 실행
        print(f"\n🚀 상품 등록 요청을 시작합니다: {product_data['originProduct']['name']}")
        try:
            result = await client.products.create_product(product_data)
            print(f"✅ 상품 등록 성공!")
            print(f"   - 스마트스토어 상품번호: {result.get('smartstoreProductNo')}")
            print(f"   - 원상품번호: {result.get('originProductNo')}")
        except Exception as e:
            print(f"❌ 상품 등록 실패:\n{e}")

if __name__ == "__main__":
    asyncio.run(register_sample_product())
