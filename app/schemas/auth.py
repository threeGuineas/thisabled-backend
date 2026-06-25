import re
import uuid

from pydantic import BaseModel, Field, field_validator

# F01_S01: 닉네임 2~12자, 한글·영문·숫자
NICKNAME_RE = re.compile(r"^[가-힣a-zA-Z0-9]{2,12}$")


def _validate_password(v: str) -> str:
    # F01_S02: 8자 이상, 영문·숫자 각 1개 이상
    if len(v) < 8:
        raise ValueError("비밀번호는 8자 이상이어야 합니다")
    if not any(c.isalpha() for c in v) or not any(c.isdigit() for c in v):
        raise ValueError("비밀번호는 영문과 숫자를 각각 포함해야 합니다")
    return v


class SignupRequest(BaseModel):
    nickname: str = Field(description="2~12자, 한글·영문·숫자", examples=["햇살가득"])
    password: str = Field(description="8자 이상, 영문+숫자 각 1개 이상", examples=["test1234"])

    @field_validator("nickname")
    @classmethod
    def _nick(cls, v: str) -> str:
        if not NICKNAME_RE.match(v):
            raise ValueError("닉네임은 2~12자의 한글·영문·숫자만 가능합니다")
        return v

    @field_validator("password")
    @classmethod
    def _pw(cls, v: str) -> str:
        return _validate_password(v)


class LoginRequest(BaseModel):
    nickname: str = Field(examples=["햇살가득"])
    password: str = Field(examples=["test1234"])


class RecoveryRequest(BaseModel):
    nickname: str = Field(examples=["햇살가득"])
    recovery_code: str = Field(description="가입 시 1회 발급된 복구 코드", examples=["A1B2-C3D4-E5F6"])
    new_password: str = Field(examples=["new1234pw"])

    @field_validator("new_password")
    @classmethod
    def _pw(cls, v: str) -> str:
        return _validate_password(v)


class CheckNicknameResponse(BaseModel):
    available: bool
    reason: str | None = Field(
        default=None,
        description="available=false 일 때 사유: duplicate | forbidden_word | invalid_format",
    )


class SignupResponse(BaseModel):
    user_id: uuid.UUID
    access_token: str
    recovery_code: str = Field(description="**재발급 불가** — 이 응답에서만 제공. 사용자에게 저장 안내 필수.")
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    access_token: str
    user_id: uuid.UUID
    needs_onboarding: bool = Field(description="true면 장애 모드 미설정 → 온보딩 화면으로 유도")
    token_type: str = "bearer"


class TokenRefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: uuid.UUID
    nickname: str
    disability_mode: str | None
    trust_score: float

    model_config = {"from_attributes": True}
