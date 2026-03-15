"""네이버 스마트스토어 Commerce API Python 클라이언트.

사용법:
    import asyncio
    from dotenv import load_dotenv
    import os
    from client import NaverCommerceClient

    load_dotenv()

    async def main():
        async with NaverCommerceClient(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
        ) as client:
            # 판매자 정보 조회 등
            result = await client.get("/v1/seller")
            print(result)

    asyncio.run(main())
"""

import asyncio
import logging
import os

from dotenv import load_dotenv

from client import NaverCommerceClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


async def main():
    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not client_id or not client_secret:
        print("ERROR: .env 파일에 CLIENT_ID, CLIENT_SECRET을 설정하세요.")
        return

    async with NaverCommerceClient(client_id, client_secret) as client:
        # 1. 토큰 발급 테스트 (내부적으로 수행됨)
        token = await client.auth.get_token()
        print(f"✅ 토큰 발급 성공: {token[:20]}...")

        # 2. 판매자 계정 정보 조회
        print("\n🔍 판매자 계정 정보 조회 중...")
        try:
            account = await client.seller.get_account()
            print("🚀 계정 정보 조회 성공!")
            print(f"결과: {account}")
        except Exception as e:
            print(f"❌ 계정 정보 조회 실패: {e}")

        # 3. 채널 정보 조회
        print("\n🔍 채널 정보 조회 중...")
        try:
            channels = await client.seller.get_channels()
            print("🚀 채널 정보 조회 성공!")
            print(f"결과: {channels}")
        except Exception as e:
            print(f"❌ 채널 정보 조회 실패: {e}")

        # 4. 상품 브랜드 조회
        print("\n🔍 상품 브랜드 조회 중...")
        try:
            brands = await client.products.get_brands(name="나이키")
            print("🚀 브랜드 조회 성공!")
            print(f"결과 수: {len(brands)}")
            if brands:
                print(f"첫 번째 결과: {brands[0]}")
        except Exception as e:
            print(f"❌ 브랜드 조회 실패: {e}")

        # 5. 사이즈 타입 조회
        print("\n🔍 사이즈 타입 조회 중...")
        try:
            sizes = await client.products.get_size_types()
            print("🚀 사이즈 타입 조회 성공!")
            print(f"결과 수: {len(sizes)}")
        except Exception as e:
            print(f"❌ 사이즈 타입 조회 실패: {e}")

        # 6. 상품 문의 조회 테스트 (간단 조회)
        print("\n🔍 최근 상품 문의 조회 중...")
        try:
            inquiries = await client.inquiries.get_product_inquiries(params={"page": 1, "size": 5})
            print("🚀 상품 문의 조회 성공!")
            print(f"결과: {inquiries.get('contents', [])}")
        except Exception as e:
            print(f"❌ 상품 문의 조회 실패: {e}")

        # 7. 일별 통계 리포트 조회 테스트
        print("\n🔍 일별 통계 리포트 헤더 조회 중...")
        try:
            # 어제 날짜 기준으로 간단 테스트 (실제 데이터 유무에 따라 응답 다를 수 있음)
            from datetime import datetime, timedelta
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            stats = await client.stats.get_all_channel_daily_report(params={"searchDate": yesterday})
            print("🚀 통계 리포트 조회 요청 성공!")
        except Exception as e:
            print(f"❌ 통계 리포트 조회 실패: {e} (권한 문제일 수 있음)")


if __name__ == "__main__":
    asyncio.run(main())
