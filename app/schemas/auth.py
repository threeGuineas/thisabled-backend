from pydantic import BaseModel, field_validator

from app.models.user import DisabilityType


class RegisterRequest(BaseModel):
    nickname: str
    password: str
    disability_type: DisabilityType = DisabilityType.none

    @field_validator("nickname")
    @classmethod
    def nickname_length(cls, v: str) -> str:
        if not 2 <= len(v) <= 50:
            raise ValueError("nickname must be 2–50 characters")
        return v

    @field_validator("password")
    @classmethod
    def password_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v


class LoginRequest(BaseModel):
    nickname: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    nickname: str
    disability_type: DisabilityType

    model_config = {"from_attributes": True}
