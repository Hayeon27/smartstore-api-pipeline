# Naver Commerce API 인증 가이드 (Auth)

## 개요
네이버 커머스 API는 OAuth 2.0 Client Credentials Grant 방식을 사용하며, 보안을 위해 bcrypt 해싱 기반의 전자서명(signature)을 요구합니다.

## 인증 절차
1. **전자서명 생성**:
   - `password`: `{CLIENT_ID}_{TIMESTAMP_MS}`
   - `salt`: `CLIENT_SECRET` (bcrypt salt 형식)
   - `signature`: `base64_encode(bcrypt.hashpw(password, salt))`
2. **토큰 요청**:
   - URL: `POST https://api.commerce.naver.com/external/v1/oauth2/token`
   - Content-Type: `application/x-www-form-urlencoded`
   - Body:
     - `client_id`: 애플리케이션 ID
     - `timestamp`: 밀리초 단위 타임스탬프
     - `client_secret_sign`: 생성된 전자서명
     - `grant_type`: `client_credentials`
     - `type`: `SELF`
3. **API 호출**:
   - Header: `Authorization: Bearer {access_token}`

## 구현 주의사항
- **토큰 유효시간**: 3시간 (10,800초)
- **갱신 정책**: 만료 30분 전부터 갱신 권장. 401 Unauthorized (`GW.AUTHN`) 발생 시 즉시 재발급 후 재시도.
- **전자서명 라이브러리**: `bcrypt`, `pybase64` 사용 권장.
