# 🚀 Naver Smartstore Commerce API Pipeline

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

네이버 커머스 API를 쉽고 강력하게 다룰 수 있는 상용 수준의 Python SDK 파이프라인입니다. 복잡한 bcrypt 전자서명부터 토큰 자동 갱신, 카테고리별 정밀 클라이언트까지 모두 포함되어 있습니다.

---

## ✨ Key Features

- **🛡️ Secure Auth**: `bcrypt` 기반 전자서명(Signature)과 OAuth2 토큰 발급/갱신 자동화.
- **🔄 Robust Request**: `tenacity` 기반의 지수 백오프 재시도 전략 및 `httpx` 비동기 통신.
- **🧩 Modular Architecture**: 공식 문서의 카테고리(상품, 주문, 문의, 물류 등)를 그대로 반영한 직관적인 모듈 구조.
- **🚀 High Performance**: `uv`를 활용한 초고속 패키지 관리 및 의존성 제어.

---

## 🏗️ Project Structure

```text
.
├── auth/            # 🔐 인증 (OAuth2, bcrypt Signature)
├── seller/          # 👤 판매자 API (계정, 채널, JWE)
├── products/        # 📦 상품 API (등록, 수정, 조회, 브랜드, 사이즈)
├── orders/          # 🛒 주문 API (목록, 상세, 발주, 발송)
├── inquiries/       # 💬 문의 API (고객 상담, 상품 Q&A)
├── logistics/       # 🚚 물류 API (SKU 관리)
├── settlement/      # 💰 정산 API (부가세, 수수료 내역)
├── statistics/      # 📊 통계 API (채널별 일별/시간대 리포트)
├── commerce/        # 🛠️ 솔루션 API (구독 관리)
├── client.py        # 🏗️ 메인 클라이언트 (NaverCommerceClient)
└── main.py          # ⚡ 실행 예제 및 테스트
```

---

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (추천)

### 2. Installation
```bash
# 저장소 클론
git clone https://github.com/Hayeon27/smartstore-api-pipeline.git
cd smartstore-api-pipeline

# 의존성 설치 (uv 사용 시)
uv sync
```

### 3. Environment Setup
`.env` 파일을 생성하고 네이버 커머스 API 센터에서 발급받은 정보를 입력하세요.
```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

---

## 💻 Usage Example

```python
import asyncio
import os
from dotenv import load_dotenv
from client import NaverCommerceClient

load_dotenv()

async def main():
    async with NaverCommerceClient(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET")
    ) as client:
        # 1. 판매자 계정 정보 조회
        account = await client.seller.get_account()
        print(f"Seller ID: {account['id']}")

        # 2. 브랜드 조회
        brands = await client.products.get_brands(name="나이키")
        print(f"Found {len(brands)} brands.")

        # 3. 주문 목록 조회 (최근 1개 예시)
        # result = await client.orders.get_product_order_ids(order_id="...")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🤝 Contributing
이 프로젝트는 네이버 커머스 API의 표준화를 지향합니다. 이슈 제보 및 Pull Request는 언제나 환영합니다.

---

## 📄 License
이 프로젝트는 [MIT License](LICENSE)를 따릅니다.