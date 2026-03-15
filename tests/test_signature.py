"""전자서명 생성 로직 검증 테스트.

공식 문서 예시 salt는 bcrypt 5.x에서 유효하지 않으므로,
정상 bcrypt salt를 생성하여 전자서명 로직 자체를 검증합니다.
실제 CLIENT_SECRET은 커머스API 센터에서 발급받은 유효한 bcrypt salt 형식입니다.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
import pybase64
from auth.token import generate_signature


def test_signature_logic():
    """전자서명 생성 로직 검증 - 정상 bcrypt salt 사용."""
    client_id = "testclientid"
    # 정상적인 bcrypt salt 생성 (실제 client_secret 형식)
    client_secret = bcrypt.gensalt(rounds=10).decode("utf-8")
    timestamp = 1643961623299

    # generate_signature 호출
    result = generate_signature(client_id, client_secret, timestamp)

    # 수동 검증: 동일한 로직으로 직접 계산
    password = f"{client_id}_{timestamp}"
    hashed = bcrypt.hashpw(password.encode("utf-8"), client_secret.encode("utf-8"))
    expected = pybase64.standard_b64encode(hashed).decode("utf-8")

    print(f"Client Secret (salt): {client_secret}")
    print(f"결과: {result}")
    print(f"기대: {expected}")
    print(f"일치: {result == expected}")
    assert result == expected, "전자서명 로직 불일치!"
    print("✅ 전자서명 로직 검증 통과")

    # Base64 디코딩 가능한지 확인
    decoded = pybase64.standard_b64decode(result)
    assert decoded.startswith(b"$2"), "bcrypt 해시 형식 불일치!"
    print("✅ Base64 디코딩 후 bcrypt 형식 확인 통과")


if __name__ == "__main__":
    test_signature_logic()
