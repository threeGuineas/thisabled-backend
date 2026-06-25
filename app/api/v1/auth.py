from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from jose import JWTError
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_recovery_code,
    hash_secret,
    verify_secret,
)
from app.db.session import get_db
from app.models.user import ForbiddenNickname, User
from app.schemas.auth import (
    CheckNicknameResponse,
    LoginRequest,
    LoginResponse,
    RecoveryRequest,
    SignupRequest,
    SignupResponse,
    TokenRefreshResponse,
    UserResponse,
)
from app.schemas.auth import NICKNAME_RE

router = APIRouter(prefix="/auth", tags=["auth"])

REFRESH_COOKIE = "refresh_token"


def _set_refresh_cookie(response: Response, user_id) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE,
        value=create_refresh_token(str(user_id)),
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        path="/api/v1/auth",
    )


async def _nickname_taken(db: AsyncSession, nickname: str) -> bool:
    existing = await db.scalar(select(User.id).where(User.nickname == nickname))
    return existing is not None


async def _nickname_forbidden(db: AsyncSession, nickname: str) -> bool:
    hit = await db.scalar(
        select(ForbiddenNickname.id).where(func.lower(ForbiddenNickname.word) == nickname.lower())
    )
    return hit is not None


@router.get(
    "/check-nickname",
    response_model=CheckNicknameResponse,
    summary="닉네임 사용 가능 여부 확인",
    description="가입 전 실시간 검증용. `available:false` 시 `reason`은 "
    "`invalid_format`(형식) · `forbidden_word`(금칙어) · `duplicate`(중복) 중 하나.",
)
async def check_nickname(nickname: str, db: AsyncSession = Depends(get_db)):
    if not NICKNAME_RE.match(nickname):
        return CheckNicknameResponse(available=False, reason="invalid_format")
    if await _nickname_forbidden(db, nickname):
        return CheckNicknameResponse(available=False, reason="forbidden_word")
    if await _nickname_taken(db, nickname):
        return CheckNicknameResponse(available=False, reason="duplicate")
    return CheckNicknameResponse(available=True)


@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    description="성공 시 `access_token` 발급 + refresh 쿠키 설정. "
    "`recovery_code`는 **이 응답에서만** 제공되며 재발급되지 않으니 사용자에게 반드시 안내·저장하게 한다.",
)
async def signup(body: SignupRequest, response: Response, db: AsyncSession = Depends(get_db)):
    if await _nickname_forbidden(db, body.nickname):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="사용할 수 없는 닉네임입니다")
    if await _nickname_taken(db, body.nickname):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용 중인 닉네임입니다")

    recovery_code = generate_recovery_code()
    user = User(
        nickname=body.nickname,
        password_hash=hash_secret(body.password),
        recovery_code_hash=hash_secret(recovery_code),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    _set_refresh_cookie(response, user.id)
    return SignupResponse(
        user_id=user.id,
        access_token=create_access_token(str(user.id)),
        recovery_code=recovery_code,
    )


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="로그인",
    description="`needs_onboarding:true` 면 장애 모드 미설정 상태 → 프론트는 온보딩(모드 선택) 화면으로 보낸다.",
)
async def login(body: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.nickname == body.nickname))
    if not user or not verify_secret(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="닉네임 또는 비밀번호가 올바르지 않습니다"
        )

    user.last_login_at = func.now()
    await db.commit()

    _set_refresh_cookie(response, user.id)
    return LoginResponse(
        access_token=create_access_token(str(user.id)),
        user_id=user.id,
        needs_onboarding=user.disability_mode is None,
    )


@router.post(
    "/refresh",
    response_model=TokenRefreshResponse,
    summary="access 토큰 갱신",
    description="httpOnly refresh 쿠키를 검증해 새 access_token 발급. 프론트는 401 발생 시 한 번 호출 후 원요청 재시도.",
)
async def refresh(refresh_token: str | None = Cookie(default=None, alias=REFRESH_COOKIE)):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="갱신 토큰이 없습니다")
    try:
        payload = decode_token(refresh_token, expected_type="refresh")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="갱신 토큰이 유효하지 않습니다")
    return TokenRefreshResponse(access_token=create_access_token(payload["sub"]))


@router.post(
    "/recovery",
    summary="복구 코드로 비밀번호 재설정",
    description="가입 시 받은 `recovery_code`로 본인 확인 후 비밀번호를 새로 설정한다.",
)
async def recovery(body: RecoveryRequest, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.nickname == body.nickname))
    if not user or not verify_secret(body.recovery_code, user.recovery_code_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="닉네임 또는 복구 코드가 올바르지 않습니다"
        )
    user.password_hash = hash_secret(body.new_password)
    await db.commit()
    return {"status": "ok"}


@router.post("/logout", summary="로그아웃", description="refresh 쿠키를 만료시킨다. access_token은 만료까지 유효하므로 프론트 저장소에서도 삭제.")
async def logout(response: Response):
    response.delete_cookie(REFRESH_COOKIE, path="/api/v1/auth")
    return {"status": "ok"}


@router.get("/me", response_model=UserResponse, summary="내 정보 조회", description="현재 access_token 소유자의 기본 정보.")
async def me(current_user: User = Depends(get_current_user)):
    return current_user
