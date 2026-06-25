from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import auth, health, posts, stt, upload, users, vision
from app.core.config import settings

# Swagger 사이드바 그룹 설명 — 프론트가 어떤 묶음을 봐야 하는지 한눈에.
tags_metadata = [
    {"name": "health", "description": "서버·DB·Redis 헬스체크. 배포/모니터링용."},
    {
        "name": "auth",
        "description": (
            "회원가입·로그인·토큰 갱신·복구. **access_token**(24h)은 응답 body로 받아 "
            "`Authorization: Bearer <token>` 헤더에 싣는다. **refresh_token**(30d)은 "
            "httpOnly 쿠키로 자동 발급되며 `/api/v1/auth/refresh` 로만 전송된다."
        ),
    },
    {"name": "users", "description": "장애 유형 모드(visual·hearing·developmental·default) 조회·변경."},
    {"name": "posts", "description": "게시글 CRUD + 피드 목록(최신순 페이지네이션)."},
    {"name": "upload", "description": "이미지 업로드. 응답 `url`(/uploads/...)을 게시글·Vision에 그대로 사용."},
    {
        "name": "vision",
        "description": (
            "시각장애 모드 — 업로드 이미지의 한국어 음성 해설(GPT-4o Vision). "
            "동일 이미지는 24h 캐싱(`cached:true`)되어 비용·지연이 0에 수렴한다."
        ),
    },
    {"name": "stt", "description": "음성 댓글·자막 — 오디오 파일을 한국어 텍스트로 전사(Whisper)."},
]

description = """
**ThisAbled** — 장애 유형별 적응형 UI 소셜 플랫폼 백엔드 API.

### 인증 흐름
1. `POST /api/v1/auth/signup` 또는 `/login` → 응답의 `access_token` 확보
   (signup 응답의 `recovery_code` 는 **재발급 불가**, 사용자에게 1회 안내).
2. 보호된 엔드포인트는 `Authorization: Bearer <access_token>` 헤더 필수.
3. access 만료(24h) 시 `POST /api/v1/auth/refresh` (httpOnly 쿠키 자동 전송)로 재발급.

### 공통 규칙
- 모든 경로 prefix: `/api/v1`
- 에러 응답 형식: `{ "detail": "<사람이 읽는 메시지>" }`
- 인증 누락·실패: `401` / 권한 없음: `403` / 검증 실패: `422`
- 시간은 UTC ISO-8601, ID는 모두 UUID.
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(
    title="ThisAbled API",
    version="0.1.0",
    description=description,
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    contact={"name": "ThisAbled Backend", "url": "https://github.com/coketazo/thisabled-backend"},
)

# refresh 토큰을 쿠키로 쓰므로 allow_credentials=True. 그래서 오리진은 와일드카드 불가.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")
app.include_router(vision.router, prefix="/api/v1")
app.include_router(stt.router, prefix="/api/v1")
