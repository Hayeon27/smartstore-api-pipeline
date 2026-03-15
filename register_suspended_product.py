"""전시/판매 중지 상태의 상품 등록 샘플 (최종 보정)."""

import asyncio
import os
import json
from dotenv import load_dotenv
from client import NaverCommerceClient

load_dotenv()

async def register_suspended_product():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    async with NaverCommerceClient(client_id, client_secret) as client:
        # 1. 주소록 정보 조회
        address_books_res = await client.seller.get_address_books()
        address_books = address_books_res.get("addressBooks", [])
        
        release_id = None
        refund_id = None
        for addr in address_books:
            if addr.get("addressType") == "RELEASE": release_id = addr.get("addressBookNo")
            if addr.get("addressType") == "REFUND_OR_EXCHANGE": refund_id = addr.get("addressBookNo")
        
        if not release_id or not refund_id:
            if address_books:
                release_id = refund_id = address_books[0].get("addressBookNo")
            else:
                print("❌ 주소록이 없습니다.")
                return

        # 2. 상품 등록 데이터 준비 (성공한 register_product_sample.py 구조와 100% 동기화)
        product_data = {
            "originProduct": {
                "statusType": "SUSPENSION", # 판매 x (판매중지)
                "saleType": "NEW",
                "leafCategoryId": "50004002",
                "name": "양말 남자", # 상품명 변경
                "detailContent": "<div class=\"se-viewer se-theme-default\" lang=\"ko-KR\"><div class=\"se-main-container\"><p>전시/판매 중정 테스트 상품입니다.</p></div></div>",
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
            "smartstoreChannelProduct": {
                "naverShoppingRegistration": False, # 전시 x
                "channelProductDisplayStatusType": "SUSPENSION" # 전시 x (전시중지)
            }
        }

        print(f"🚀 상품 등록 재시도: {product_data['originProduct']['name']} (상태: 중지)")
        try:
            result = await client.products.create_product(product_data)
            print(f"✅ 상품 등록 성공!")
            print(f"   - 원상품번호: {result.get('originProductNo')}")
        except Exception as e:
            print(f"❌ 상품 등록 실패:\n{e}")

if __name__ == "__main__":
    asyncio.run(register_suspended_product())
