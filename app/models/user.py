import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Uuid, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nickname: Mapped[str] = mapped_column(String(12), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    recovery_code_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    # null = 온보딩 미완료 → 로그인 시 needs_onboarding=true
    disability_mode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    mode_settings: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default=text("'{}'"))
    trust_score: Mapped[float] = mapped_column(Float, nullable=False, server_default=text("1.0"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ForbiddenNickname(Base):
    """운영자 관리 금칙어 사전. check-nickname 시 forbidden_word 판정 근거."""

    __tablename__ = "forbidden_nicknames"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class UserModeHistory(Base):
    """모드 변경 이력 (F02_S08, 베타테스트 분석용)."""

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
