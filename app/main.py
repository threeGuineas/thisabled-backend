from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import health
from app.core.config import settings

# v2.1 리팩토링 진행 중 — 라우터는 도메인 태스크마다 재등록한다.
# (docs/superpowers/plans/2026-07-05-v2_1-refactor.md)
tags_metadata = [
    {"name": "health", "description": "서버·DB·Redis 헬스체크. 배포/모니터링용."},
]

description = """
**ThisAbled** — 장애 유형별 적응형 UI 소셜 플랫폼 백엔드 API (명세 v2.1).

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
    version="0.2.0",
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
