# 🛠️ 유틸리티 및 디버깅 가이드

개발 및 운영 과정에서 데이터를 검증하고 문제 원인을 파악하기 위한 도구들입니다.

## 🔍 DB 데이터 물리적 검증
`pipeline.runner` 실행 후 실제 SQLite 데이터베이스에 레코드가 생성되었는지 테이블별로 출력합니다.
- **커맨드**: `uv run python check_db.py`
- **확인 항목**: `products`, `orders`, `inquiries` 테이블의 로우 수 및 샘플 데이터.

## 🐞 API 수집 정밀 분석
수집 과정에서 데이터가 누락되거나 API 에러가 발생할 때 사용합니다.
- **[debug_etl.py](../debug_etl.py)**: HTTP 요청 파라미터와 인코딩 상태를 상세 로깅합니다.
- **[debug_keys.py](../debug_keys.py)**: API 응답 JSON의 실제 필드명(Case-sensitive)을 추출하여 매핑 오류를 찾습니다.

## 📋 상품 상태 교차 체크
원상품과 채널상품 간의 전시 상태 불일치 문제를 해결하기 위해 사용합니다.
- **커맨드**: `uv run python check_status.py`
- **대상**: 특정 `originProductNo`를 기준으로 서버의 원본 데이터와 채널별 전시 데이터를 대조 출력합니다.

[README로 돌아가기](../README.md)
