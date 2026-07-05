"""스키마 v3 baseline 정합 검증 (설계: docs/superpowers/specs/2026-07-05-v2_1-refactor-design.md §1)."""

import app.models as m


def test_v3_models_registered():
    from app.db.session import Base

    names = set(Base.metadata.tables)
    assert {
        "users", "social_identities", "withdrawn_socials", "interest_tags",
        "user_interest_tags", "forbidden_nicknames", "user_mode_history",
        "posts", "post_media", "comments", "post_likes",
        "friend_requests", "friendships", "blocks",
        "chat_rooms", "chat_messages", "send_restrictions",
        "notifications", "ai_result_cache",
    } <= names
    # 신고는 MVP 제외(§3.2), 구 messages 테이블은 chat_messages로 대체
    assert "reports" not in names
    assert "messages" not in names


def test_users_v3_columns():
    cols = {c.name for c in m.User.__table__.columns}
    # 소셜 전용 인증 — 비밀번호·복구코드 없음 (ACC-01/02)
    assert "password_hash" not in cols
    assert "recovery_code_hash" not in cols
    assert "trust_score" not in cols
    assert {"birth_date", "ui_mode", "bio", "profile_image_url",
            "stranger_requests_allowed", "mode_settings", "risk_score"} <= cols


def test_anonymizable_fks_nullable():
    """탈퇴 익명화(§15): 게시물·댓글·채팅 발신자는 SET NULL 가능해야 한다."""
    assert m.Post.__table__.c.author_id.nullable
    assert m.Comment.__table__.c.author_id.nullable
    assert m.ChatMessage.__table__.c.sender_id.nullable
