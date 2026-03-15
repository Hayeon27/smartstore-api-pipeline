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
        # 토큰 발급 테스트
        token = await client.auth.get_token()
        print(f"토큰 발급 성공: {token[:20]}...")


if __name__ == "__main__":
    asyncio.run(main())
