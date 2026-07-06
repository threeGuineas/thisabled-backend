"""v2.1 명세 고정값이 Settings에 반영되어 있는지 검증."""

from app.core.config import Settings, settings


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


def test_settings_ignores_compose_only_env_vars(monkeypatch):
    """docker compose env_file은 POSTGRES_PASSWORD/REDIS_PASSWORD도 컨테이너 프로세스에 노출한다.
    이 값들은 compose 변수 치환용일 뿐 Settings 필드가 아니므로 extra=forbid면 부팅이 죽는다."""
    monkeypatch.setenv("POSTGRES_PASSWORD", "irrelevant-to-app")
    monkeypatch.setenv("REDIS_PASSWORD", "irrelevant-to-app")
    Settings(DATABASE_URL=settings.DATABASE_URL, REDIS_URL=settings.REDIS_URL, SECRET_KEY=settings.SECRET_KEY)
