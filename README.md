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
├── seller/          # 👤 판매자 API (계정, 채널, 주소록)
├── products/        # 📦 상품 API (등록, 수정, 조회, 브랜드)
├── orders/          # 🛒 주문 API (목록, 상세, 발주)
├── inquiries/       # 💬 문의 API (고객 상담, 상품 Q&A)
├── pipeline/        # 🔄 ETL 파이프라인 (Extractor, Storage)
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
git clone https://github.com/Hayeon27/smartstore-api-pipeline.git
cd smartstore-api-pipeline
uv sync
```

### 3. Environment Setup
`.env` 파일을 생성하고 정보를 입력하세요.
```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

---

## 🚀 Quick Execution Guide

본 레포지토리에 포함된 핵심 자동화 스크립트들입니다. 하이퍼링크를 클릭하시면 소스 코드를 확인하실 수 있습니다.

| Category | Command | Description |
| :--- | :--- | :--- |
| **Test** | `uv run python main.py` | [연결성 테스트](main.py) - 전체 API 정상 동작 확인 |
| **Pipeline** | `uv run python -m pipeline.runner` | [데이터 수집](pipeline/runner.py) - API 데이터를 로컬 DB로 적재 |
| **Registration** | `uv run python register_product_sample.py` | [상품 등록](register_product_sample.py) - 신규 상품 가이드 |
| **Management** | `uv run python register_suspended_product.py` | [중지 등록](register_suspended_product.py) - 전시/판매 중지 상품 등록 |
| **Utility** | `uv run python check_db.py` | [DB 확인](check_db.py) - SQLite 적재 데이터 물리적 검증 |
| **Debug** | `uv run python check_status.py` | [상태 체크](check_status.py) - 특정 상품의 상세 상태 대조 |

---

## 💻 Usage Example

```python
async with NaverCommerceClient(client_id, client_secret) as client:
    # 예: 판매자 주소록 조회
    address_books = await client.seller.get_address_books()
    
    # 예: 원상품 조회 (v2)
    product = await client.products.get_origin_product("13195917377")
```

---

## 🤝 Contributing
이 프로젝트는 네이버 커머스 API의 표준화를 지향합니다. 이슈 제보 및 Pull Request는 언제나 환영합니다.

---

## 📄 License
이 프로젝트는 [MIT License](LICENSE)를 따릅니다.