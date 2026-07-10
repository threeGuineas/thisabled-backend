import uuid
from datetime import datetime, timezone


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
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


class ChatRoom(Base):
    """1:1 채팅방 (CHAT-01/02). request=요청함, active=일반 채팅.

    참여자는 정규화 쌍(user_a < user_b, 앱에서 보장). 탈퇴 시 SET NULL 익명화 —
    상대방의 대화 기록 보존(§15).
    """

    __tablename__ = "chat_rooms"
    __table_args__ = (UniqueConstraint("user_a", "user_b"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_a: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    user_b: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    state: Mapped[str] = mapped_column(String(20), nullable=False)
    requested_by: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ChatMessage(Base):
    """채팅 메시지 (SAFE-01~03). 텍스트는 동기 분석 후 저장·전달."""

    __tablename__ = "chat_messages"
    __table_args__ = (Index("ix_chat_messages_room_created", "room_id", "created_at"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    room_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_rooms.id", ondelete="CASCADE"), nullable=False
    )
    # 탈퇴 익명화(§15): SET NULL → '탈퇴한 사용자'
    sender_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    type: Mapped[str] = mapped_column(String(10), nullable=False, server_default=text("'text'"))
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    media_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    # 채팅 사진 설명(VISION-01)·영상 자막(CAPTION-01) — 즉시 전달 후 비동기 부착
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'none'")
    )
    caption: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    caption_status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'none'")
    )
    # SAFE: pending(비친구 보류)|safe|flagged|unanalyzed(§18.3 성능저하)
    safety_status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    # SAFE-03 '내용 보기' 실행 시각. 실행해도 SAFE-05 집계에는 포함(§SAFE-05-6)
    revealed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    available_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # python default: SAFE-05 누적 경계 비교에 실제 시각 필요 —
    # server_default(now())는 트랜잭션 시작 시각으로 고정되어 released_at 경계와 어긋난다
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, server_default=func.now(), nullable=False
    )


class ChatReadState(Base):
    """사용자별 채팅방 읽음 커서."""

    __tablename__ = "chat_read_states"
    __table_args__ = (
        UniqueConstraint("room_id", "user_id"),
        Index("ix_chat_read_states_user_room", "user_id", "room_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    room_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_rooms.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    last_read_message_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    last_read_available_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class SendRestriction(Base):
    """SAFE-05 관계 단위 자동 전송 제한.

    누적 카운터는 별도 컬럼 없이 chat_messages에서
    `flagged AND created_at > max(now - 3일, 마지막 released_at)` 쿼리로 계산.
    해제(released_at 기록) = 카운터 리셋 경계.
    """

    __tablename__ = "send_restrictions"
    __table_args__ = (Index("ix_send_restrictions_pair", "sender_id", "receiver_id", "active"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    sender_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    receiver_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    released_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
