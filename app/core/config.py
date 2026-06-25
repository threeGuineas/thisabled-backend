from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    # F01_S04: access 24시간, refresh 30일
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    COOKIE_SECURE: bool = False  # 운영(HTTPS)에서는 true
    # 프론트 오리진(쉼표 구분). refresh 쿠키를 쓰므로 allow_credentials=True 와 함께
    # 와일드카드(*) 대신 명시적 오리진만 허용한다.
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    STORAGE_BACKEND: str = "local"
    UPLOAD_DIR: str = "/app/uploads"
    MAX_UPLOAD_MB: int = 10
    # F02_S04 시각장애 모드 — GPT-4o Vision 이미지 해설
    OPENAI_API_KEY: str | None = None
    VISION_MODEL: str = "gpt-4o"
    VISION_MAX_TOKENS: int = 300
    VISION_CACHE_TTL_SECONDS: int = 60 * 60 * 24  # 동일 이미지 24h 캐싱(비용 방어)
    # F02_S05 — Whisper STT (음성 댓글 / 자막)
    STT_MODEL: str = "whisper-1"
    MAX_AUDIO_MB: int = 25  # Whisper API 업로드 상한

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
