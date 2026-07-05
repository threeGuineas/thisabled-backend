"""v2.1 명세 고정값이 Settings에 반영되어 있는지 검증."""

from app.core.config import settings


def test_v2_1_settings_defaults():
    assert settings.SAFE_FLAG_WINDOW_DAYS == 3
    assert settings.SAFE_FLAG_LIMIT == 3
    assert settings.VISION_DAILY_LIMIT == 20
    assert settings.VISION_MINUTE_LIMIT == 5
    assert settings.CAPTION_DAILY_LIMIT == 5
    assert settings.REJOIN_BLOCK_DAYS == 30
    assert settings.DRAFT_TTL_HOURS == 24
    assert settings.COMM_CONTEXT_MESSAGES == 10
    assert settings.SAFETY_TIMEOUT_SECONDS == 2.0
    assert settings.AI_RETRY_MAX == 2
    assert settings.MAX_VIDEO_MB == 200
    assert settings.MAX_VIDEO_SECONDS == 180
    assert settings.SIGNUP_TOKEN_EXPIRE_MINUTES == 30
    assert settings.OAUTH_MOCK is True
    assert settings.SAFETY_MODEL_URL.startswith("http")
    assert settings.MATCH_MODEL_URL.startswith("http")
