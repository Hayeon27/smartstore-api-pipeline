"""bcrypt salt 형식 확인."""

import bcrypt

# bcrypt로 정상 salt 생성
generated_salt = bcrypt.gensalt(rounds=10)
print(f"Generated salt: {generated_salt}")
print(f"Generated salt length: {len(generated_salt)}")

# 문서 예시 salt와 비교
doc_salt = b"$2a$10$abcdefghijklmnopqrstuv"
print(f"Doc salt: {doc_salt}")
print(f"Doc salt length: {len(doc_salt)}")

# bcrypt salt는 $2b$XX$ + 22자 = 29자여야 함
# 문서 예시 salt의 22자 부분: "abcdefghijklmnopqrstuv" = 22자, OK
# 문제: bcrypt 5.x에서는 $2a$ prefix를 $2b$로 변경 해야할 수도

# $2b$로 시도
salt_2b = b"$2b$10$abcdefghijklmnopqrstuv"
print(f"2b salt: {salt_2b}")
try:
    hashed = bcrypt.hashpw(b"test", salt_2b)
    print(f"$2b$ hashed OK: {hashed}")
except Exception as e:
    print(f"$2b$ error: {e}")

# $2a$로 시도
try:
    hashed = bcrypt.hashpw(b"test", doc_salt)
    print(f"$2a$ hashed OK: {hashed}")
except Exception as e:
    print(f"$2a$ error: {e}")

# 정상적인 salt로 해싱
try:
    hashed = bcrypt.hashpw(b"test", generated_salt)
    print(f"Generated salt hashed OK: {hashed}")
except Exception as e:
    print(f"Generated salt error: {e}")
