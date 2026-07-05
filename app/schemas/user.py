import uuid
from typing import Literal

from pydantic import BaseModel, Field

from app.core.enums import UiMode


class TagOut(BaseModel):
    code: str
    category: str
    label: str


class TagCatalogOut(BaseModel):
    tags: list[TagOut]


class MeOut(BaseModel):
    """본인 조회 — ui_mode·is_minor 등 민감 파생값 포함 (타인 조회와 분리)."""

    id: uuid.UUID
    nickname: str
    bio: str | None
    profile_image_url: str | None
    ui_mode: str
    is_minor: bool
    stranger_requests_allowed: bool
    mode_settings: dict
    tags: list[TagOut]


class PublicProfileOut(BaseModel):
    """타인 프로필 — 장애 유형·UI 모드·생년월일 비노출 (ACC-03, §5.2)."""

    id: uuid.UUID
    nickname: str
    bio: str | None
    profile_image_url: str | None
    tags: list[TagOut]


class ProfilePatchIn(BaseModel):
    nickname: str | None = Field(default=None, min_length=2, max_length=12)
    bio: str | None = Field(default=None, max_length=300)
    profile_image_url: str | None = None


class TagsPutIn(BaseModel):
    tag_codes: list[str]


class SettingsPatchIn(BaseModel):
    stranger_requests_allowed: bool | None = None
    mode_settings: dict | None = None


class ModePutIn(BaseModel):
    ui_mode: UiMode


class WithdrawIn(BaseModel):
    """§15: 게시물·댓글을 '탈퇴한 사용자'로 남길지 함께 지울지 탈퇴 화면에서 선택."""

    posts_action: Literal["anonymize", "delete"] = "anonymize"
