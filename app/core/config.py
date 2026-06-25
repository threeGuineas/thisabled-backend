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
    STORAGE_BACKEND: str = "local"
    UPLOAD_DIR: str = "/app/uploads"
    MAX_UPLOAD_MB: int = 10
    # F02_S04 시각장애 모드 — GPT-4o Vision 이미지 해설
    OPENAI_API_KEY: str | None = None
    VISION_MODEL: str = "gpt-4o"
    VISION_MAX_TOKENS: int = 300
    VISION_CACHE_TTL_SECONDS: int = 60 * 60 * 24  # 동일 이미지 24h 캐싱(비용 방어)


settings = Settings()
