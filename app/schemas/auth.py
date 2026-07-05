import uuid
from datetime import date

from pydantic import BaseModel, Field

from app.core.enums import UiMode


class AuthorizeOut(BaseModel):
    authorize_url: str


class CallbackOut(BaseModel):
    is_new_user: bool
    # 기가입자: 즉시 로그인
    access_token: str | None = None
    token_type: str = "bearer"
    user_id: uuid.UUID | None = None
    # 신규: 추가 정보 입력 단계로
    signup_token: str | None = None


class Agreements(BaseModel):
    """가입 필수 동의 3종 (ACC-01, §17 외부 AI 데이터 처리 안내 포함)."""

    terms: bool
    privacy: bool
    ai_notice: bool


class SignupIn(BaseModel):
    signup_token: str
    nickname: str = Field(min_length=2, max_length=12)
    birth_date: date
    ui_mode: UiMode
    agreements: Agreements


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: uuid.UUID
    stranger_requests_allowed: bool


class AccessTokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
