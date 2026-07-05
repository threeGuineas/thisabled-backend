"""ACC-01/02 — 소셜 OAuth 전용 인증.

흐름: authorize → 제공자 로그인 → callback
  - 기가입자: 즉시 로그인 (access body + refresh httpOnly 쿠키)
  - 신규: signup_token(30분) → POST /signup (추가 정보 + 약관) → 가입 완료
"""

import secrets
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.age import full_age, is_minor
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_signup_token,
    decode_signup_token,
    decode_token,
)
from app.db.session import get_db
from app.models import SocialIdentity, User, WithdrawnSocial
from app.schemas.auth import AccessTokenOut, AuthorizeOut, CallbackOut, SignupIn, TokenOut
from app.services.nickname import validate_nickname
from app.services.oauth import get_provider

router = APIRouter(prefix="/auth", tags=["auth"])

_REFRESH_COOKIE = "refresh_token"


def _set_refresh_cookie(response: Response, user_id: uuid.UUID) -> None:
    # COOKIE_SECURE=true(HTTPS 크로스사이트)면 SameSite=None 필요 — dcf4a31 참조
    response.set_cookie(
        key=_REFRESH_COOKIE,
        value=create_refresh_token(str(user_id)),
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="none" if settings.COOKIE_SECURE else "lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/api/v1/auth",
    )


@router.get("/{provider}/authorize", response_model=AuthorizeOut)
async def authorize(provider: str):
    p = get_provider(provider)
    return AuthorizeOut(authorize_url=p.authorize_url(state=secrets.token_urlsafe(16)))


@router.get("/{provider}/callback", response_model=CallbackOut)
async def callback(provider: str, code: str, response: Response, db: AsyncSession = Depends(get_db)):
    p = get_provider(provider)
    try:
        info = await p.exchange_code(code)
    except ValueError:
        raise HTTPException(status_code=400, detail="소셜 인증에 실패했습니다. 다시 시도해 주세요")

    identity = (
        await db.execute(
            select(SocialIdentity).where(
                SocialIdentity.provider == info.provider,
                SocialIdentity.provider_user_id == info.provider_user_id,
            )
        )
    ).scalar_one_or_none()

    if identity is None:
        # 신규 — 추가 정보 입력 단계로 (ACC-01 시나리오 3)
        return CallbackOut(
            is_new_user=True,
            signup_token=create_signup_token(info.provider, info.provider_user_id),
        )

    user = await db.get(User, identity.user_id)
    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()
    _set_refresh_cookie(response, user.id)
    return CallbackOut(
        is_new_user=False, access_token=create_access_token(str(user.id)), user_id=user.id
    )


@router.post("/signup", response_model=TokenOut, status_code=201)
async def signup(body: SignupIn, response: Response, db: AsyncSession = Depends(get_db)):
    try:
        provider, provider_user_id = decode_signup_token(body.signup_token)
    except (JWTError, KeyError):
        raise HTTPException(status_code=401, detail="가입 세션이 만료됐습니다. 처음부터 다시 시도해 주세요")

    a = body.agreements
    if not (a.terms and a.privacy and a.ai_notice):
        raise HTTPException(status_code=400, detail="필수 약관에 모두 동의해야 가입할 수 있습니다")

    if full_age(body.birth_date) < 14:
        raise HTTPException(status_code=400, detail="만 14세 이상만 가입할 수 있습니다")

    # §15: 동일 소셜 계정 탈퇴 후 30일 재가입 제한
    rejoin_limit = datetime.now(timezone.utc) - timedelta(days=settings.REJOIN_BLOCK_DAYS)
    recent_withdrawal = (
        await db.execute(
            select(WithdrawnSocial.id).where(
                WithdrawnSocial.provider == provider,
                WithdrawnSocial.provider_user_id == provider_user_id,
                WithdrawnSocial.withdrawn_at > rejoin_limit,
            )
        )
    ).scalar_one_or_none()
    if recent_withdrawal is not None:
        raise HTTPException(status_code=403, detail="탈퇴 후 30일간 재가입할 수 없습니다")

    # 콜백 이후 동일 계정이 먼저 가입을 끝낸 경우
    existing = (
        await db.execute(
            select(SocialIdentity.id).where(
                SocialIdentity.provider == provider,
                SocialIdentity.provider_user_id == provider_user_id,
            )
        )
    ).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=409, detail="이미 가입된 소셜 계정입니다. 로그인해 주세요")

    await validate_nickname(db, body.nickname)

    user = User(
        id=uuid.uuid4(),
        nickname=body.nickname,
        birth_date=body.birth_date,
        ui_mode=body.ui_mode.value,
        # §4.5: 미성년은 성인 발신 비친구 요청 기본 차단
        stranger_requests_allowed=not is_minor(body.birth_date),
        last_login_at=datetime.now(timezone.utc),
    )
    db.add(user)
    # relationship() 미사용 모델은 mapper 간 insert 순서가 보장되지 않는다 —
    # 부모(users) 먼저 flush 후 자식(social_identities) 추가 (레포 컨벤션)
    await db.flush()
    db.add(
        SocialIdentity(
            id=uuid.uuid4(),
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id,
        )
    )
    await db.commit()

    _set_refresh_cookie(response, user.id)
    return TokenOut(
        access_token=create_access_token(str(user.id)),
        user_id=user.id,
        stranger_requests_allowed=user.stranger_requests_allowed,
    )


@router.post("/refresh", response_model=AccessTokenOut)
async def refresh(
    db: AsyncSession = Depends(get_db),
    refresh_token: str | None = Cookie(default=None, alias=_REFRESH_COOKIE),
):
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = decode_token(refresh_token, expected_type="refresh")
        user_id = uuid.UUID(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")
    if await db.get(User, user_id) is None:
        raise HTTPException(status_code=401, detail="User not found")
    return AccessTokenOut(access_token=create_access_token(str(user_id)))


@router.post("/logout", status_code=204)
async def logout(response: Response):
    response.delete_cookie(_REFRESH_COOKIE, path="/api/v1/auth")
    return Response(status_code=204)
