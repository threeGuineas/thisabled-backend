"""JWT 토큰 (access/refresh/signup). 소셜 OAuth 전용이라 비밀번호 해시는 없다 (ACC-01)."""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


def _encode(claims: dict, token_type: str, delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {**claims, "type": token_type, "iat": now, "exp": now + delta},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_access_token(subject: str) -> str:
    return _encode(
        {"sub": str(subject)}, "access", timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(subject: str) -> str:
    return _encode(
        {"sub": str(subject)}, "refresh", timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


def create_signup_token(provider: str, provider_user_id: str) -> str:
    """콜백에서 신규 사용자에게 발급 — 추가 정보 입력(signup) 완료까지의 단기 자격."""
    return _encode(
        {"sub": provider_user_id, "provider": provider},
        "signup",
        timedelta(minutes=settings.SIGNUP_TOKEN_EXPIRE_MINUTES),
    )


def decode_token(token: str, expected_type: str | None = None) -> dict:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    if expected_type is not None and payload.get("type") != expected_type:
        raise JWTError(f"expected {expected_type} token")
    return payload


def decode_signup_token(token: str) -> tuple[str, str]:
    """→ (provider, provider_user_id). 위조·만료 시 JWTError."""
    payload = decode_token(token, expected_type="signup")
    return payload["provider"], payload["sub"]
