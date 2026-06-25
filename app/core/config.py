from pydantic_settings import BaseSettings


class Settings(BaseSettings):
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

    class Config:
        env_file = ".env"


settings = Settings()
