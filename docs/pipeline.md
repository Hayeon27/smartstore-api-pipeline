# 🔄 데이터 파이프라인 (ETL) 가이드

네이버 스마트스토어의 상품, 주문, 문의 데이터를 자동으로 수집하여 로컬 데이터베이스에 적재하는 시스템입니다.

## 🏗️ 구성 요소
- **[Extractor](../pipeline/extractor.py)**: API로부터 데이터를 추출하고 페이지네이션을 처리합니다.
- **[Storage](../pipeline/storage.py)**: SQLite를 사용하여 데이터를 저장하며, 기존 데이터가 있을 경우 업데이트(Upsert)합니다.
- **[Runner](../pipeline/runner.py)**: 수집 프로세스를 실행하고 로그를 기록합니다.

## 🚀 수집 실행
전체 데이터를 동기화하려면 아래 커맨드를 실행하세요.
```bash
uv run python -m pipeline.runner
```

## 🗄️ 데이터 확인
로컬 DB(`data/smartstore.db`)에 실제 데이터가 들어갔는지 육안으로 확인하려면 유틸리티를 실행하세요.
```bash
uv run python check_db.py
```

## ⚠️ 주의사항
- 한 번에 대량의 데이터를 수집할 경우 API 호출 제한(Rate Limit)이 발생할 수 있습니다. `tenacity`가 이를 처리하지만, 수만 건 이상의 경우 실행 주기를 조절하는 것이 좋습니다.
- 기본적으로 상품 검색 결과의 첫 번째 채널 정보를 대표 데이터로 저장합니다.

[README로 돌아가기](../README.md)
