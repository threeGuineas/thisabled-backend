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

    # ── v2.1 (docs/ThisAbled_기능명세서_v2_1.md) ──────────────────────
    # OAuth (ACC-01): dev는 mock 제공자, 실키 발급 후 환경변수 교체
    OAUTH_MOCK: bool = True
    KAKAO_CLIENT_ID: str | None = None
    KAKAO_CLIENT_SECRET: str | None = None
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    OAUTH_REDIRECT_BASE: str = "http://localhost:8000"
    SIGNUP_TOKEN_EXPIRE_MINUTES: int = 30
    REJOIN_BLOCK_DAYS: int = 30  # §15 탈퇴 후 재가입 제한

    # SAFE — 자체 안전 모델 (별도 모델 서버 HTTP 경계)
    SAFETY_MODEL_URL: str = "http://safety-model:9001"
    SAFETY_TIMEOUT_SECONDS: float = 2.0  # 초과 시 §18.3 성능저하 모드
    SAFE_FLAG_WINDOW_DAYS: int = 3  # SAFE-05 누적 기간
    SAFE_FLAG_LIMIT: int = 3  # SAFE-05 누적 횟수

    # MATCH — SBERT+LightGBM 모델 서버
    MATCH_MODEL_URL: str = "http://match-model:9002"

    # VISION-01 / CAPTION-01 호출 한도 (게시물·채팅 합산)
    VISION_DAILY_LIMIT: int = 20
    VISION_MINUTE_LIMIT: int = 5
    CAPTION_DAILY_LIMIT: int = 5
    AI_RETRY_MAX: int = 2
    MAX_VIDEO_MB: int = 200
    MAX_VIDEO_SECONDS: int = 180
    DRAFT_TTL_HOURS: int = 24  # POST-01 내부 드래프트 수명

    # COMM-05: 버튼 실행 시 외부 LLM에 전달하는 최근 메시지 수
    COMM_CONTEXT_MESSAGES: int = 10

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
