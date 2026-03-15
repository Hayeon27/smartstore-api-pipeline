"""네이버 커머스API 커스텀 예외 클래스."""


class NaverAPIError(Exception):
    """네이버 커머스API 기본 에러."""

    def __init__(self, status_code: int, code: str, message: str, trace_id: str = ""):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.trace_id = trace_id
        super().__init__(f"[{status_code}] {code}: {message} (traceId={trace_id})")


class AuthenticationError(NaverAPIError):
    """인증 관련 에러 (401, GW.AUTHN)."""
    pass


class RateLimitError(NaverAPIError):
    """요청 제한 에러 (429)."""
    pass


class ValidationError(NaverAPIError):
    """유효성 검사 에러 (400)."""
    pass
