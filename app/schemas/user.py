import uuid
from typing import Literal

from pydantic import BaseModel, Field

from app.core.enums import UiMode
from app.schemas.common import StrictRequest


class TagOut(BaseModel):
    code: str
    category: str
    label: str


class TagCatalogOut(BaseModel):
    tags: list[TagOut]


class ProfileStatsOut(BaseModel):
    post_count: int
    comment_count: int
    received_like_count: int


class ProfileRelationshipOut(BaseModel):
    status: Literal["self", "none", "request_sent", "request_received", "friends"]
    request_id: uuid.UUID | None = None


class NotificationSettingsOut(BaseModel):
    friend_activity: bool = True
    post_activity: bool = True
    chat_activity: bool = True
    ai_results: bool = True


class NotificationSettingsPatch(StrictRequest):
    friend_activity: bool | None = None
    post_activity: bool | None = None
    chat_activity: bool | None = None
    ai_results: bool | None = None


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
    notification_settings: NotificationSettingsOut
    tags: list[TagOut]
    stats: ProfileStatsOut


class PublicProfileOut(BaseModel):
    """타인 프로필 — 장애 유형·UI 모드·생년월일 비노출 (ACC-03, §5.2)."""

    id: uuid.UUID
    nickname: str
    bio: str | None
    profile_image_url: str | None
    tags: list[TagOut]
    stats: ProfileStatsOut
    relationship: ProfileRelationshipOut


class ProfilePatchIn(StrictRequest):
    nickname: str | None = Field(default=None, min_length=2, max_length=12)
    bio: str | None = Field(default=None, max_length=300)
    profile_image_url: str | None = Field(default=None, max_length=2048)


class TagsPutIn(StrictRequest):
    tag_codes: list[str]


class SettingsPatchIn(StrictRequest):
    stranger_requests_allowed: bool | None = None
    mode_settings: dict | None = None
    notification_settings: NotificationSettingsPatch | None = None


class ModePutIn(StrictRequest):
    ui_mode: UiMode


class WithdrawIn(StrictRequest):
    """§15: 게시물·댓글을 '탈퇴한 사용자'로 남길지 함께 지울지 탈퇴 화면에서 선택."""

    posts_action: Literal["anonymize", "delete"] = "anonymize"
