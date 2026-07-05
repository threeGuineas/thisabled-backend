import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class User(Base):
    """서비스 사용자 (ACC-01). 만 나이·연령대·미성년 여부는 저장하지 않고 birth_date로 계산."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nickname: Mapped[str] = mapped_column(String(12), unique=True, nullable=False, index=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    # §18.3: 장애 유형 원본은 저장하지 않는다. 사용자가 선택한 UI 모드만.
    ui_mode: Mapped[str] = mapped_column(String(20), nullable=False)
    bio: Mapped[str | None] = mapped_column(String(300), nullable=True)
    profile_image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    # §4.5: 가입 시 성인 true / 미성년 false로 초기화, 본인이 변경 가능
    stranger_requests_allowed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true")
    )
    mode_settings: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default=text("'{}'"))
    # SAFE-04: 발신자 단위 내부 위험 점수 (사용자 비노출)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, server_default=text("0.0"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class SocialIdentity(Base):
    """소셜 계정 연결 (ACC-01). 사용자 1명이 복수 제공자 연결 가능."""

    __tablename__ = "social_identities"
    __table_args__ = (UniqueConstraint("provider", "provider_user_id"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider: Mapped[str] = mapped_column(String(20), nullable=False)
    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class WithdrawnSocial(Base):
    """§15: 탈퇴 후 30일 재가입 제한 판정용. users 행은 hard delete하고 여기에만 흔적."""

    __tablename__ = "withdrawn_socials"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    provider: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    withdrawn_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class InterestTag(Base):
    """TAG-01 관심사 태그 카탈로그 (10 카테고리, baseline 마이그레이션 시드)."""

    __tablename__ = "interest_tags"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(40), nullable=False)
    label: Mapped[str] = mapped_column(String(40), nullable=False)


class UserInterestTag(Base):
    """사용자-태그 선택 (최대 10개는 앱 검증)."""

    __tablename__ = "user_interest_tags"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("interest_tags.id", ondelete="CASCADE"), primary_key=True
    )


class ForbiddenNickname(Base):
    """운영자 관리 금칙어 사전 (ACC-01 닉네임 정책)."""

    __tablename__ = "forbidden_nicknames"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class UserModeHistory(Base):
    """모드 변경 이력 (§5.2, 베타테스트 분석용)."""

    __tablename__ = "user_mode_history"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    from_mode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    to_mode: Mapped[str] = mapped_column(String(20), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
