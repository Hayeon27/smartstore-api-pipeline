# 🛡️ 상품 등록 안전 가이드 (Safety First)

이 프로젝트는 테스트 과정에서 실제 구매가 발생하는 사고를 방지하기 위해 **Safety First** 원칙을 따릅니다.

## 📌 기본 원칙
1.  **비전시/판매중지 기본값**: 모든 테스트용 상품 등록 스크립트는 `statusType: SUSPENSION` 및 `channelProductDisplayStatusType: SUSPENSION`을 기본값으로 사용합니다.
2.  **검색 제외**: 네이버 쇼핑 등록(`naverShoppingRegistration`)은 검색봇에 잡히지 않도록 `False`로 설정합니다.

## 🛠️ 상태 변경 방법
테스트 완료 후 실제 판매를 원하실 경우 아래 단계를 따르세요.

### 1. 스크립트 수정
`register_product_sample.py` 또는 `demo_e2e.py` 내의 상태값을 변경합니다.
```python
"statusType": "SALE", # SUSPENSION -> SALE
...
"channelProductDisplayStatusType": "ON" # SUSPENSION -> ON
```

### 2. v2 수정 API 활용
이미 등록된 상품은 `update_status_v2.py` 예제를 참고하여 일괄 변경할 수 있습니다.

> [!WARNING]
> 전시(`ON`) 상태로 변경하는 순간 실제 사용자에게 상품이 노출되며 구매가 발생할 수 있습니다. 가격 및 재고 설정을 반드시 확인하세요.

[README로 돌아가기](../README.md)
