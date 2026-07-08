from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import (
    auth,
    blocks,
    chat,
    comm,
    friends,
    health,
    media,
    notifications,
    posts,
    recommendations,
    users,
    ws,
)
from app.core.config import settings

# Swagger 사이드바 그룹 설명 — 프론트가 어떤 묶음을 봐야 하는지 한눈에.
# SSOT: docs/ThisAbled_기능명세서_v2_1.md / 요약: docs/api.md
tags_metadata = [
    {"name": "health", "description": "서버·DB·Redis 헬스체크. 배포/모니터링용."},
    {
        "name": "auth",
        "description": (
            "소셜 OAuth 전용 인증 (ACC-01/02). authorize → callback → FRONTEND_URL로 302 "
            "(기가입자 `?is_new_user=false&access_token=…`, 신규 `?is_new_user=true&signup_token=…`(30분), "
            "오류·거부 `?error={provider}_failed`). "
            "**access_token**(24h)은 쿼리/body, **refresh_token**(30d)은 httpOnly 쿠키. "
            "dev는 mock 제공자(code=`mock:<uid>`), 실키는 환경변수 교체."
        ),
    },
    {
        "name": "users",
        "description": "프로필·TAG-01 관심사·설정·UI 모드 변경(§5.2)·회원 탈퇴(§15). 타인 프로필에는 모드·생년월일 비노출.",
    },
    {
        "name": "posts",
        "description": (
            "피드(FEED-01, published만·차단 제외)·게시물 CRUD·좋아요·댓글(POST-01~03). "
            "영상 드래프트는 publish로만 공개 — AI가 게시를 대신하지 않는다(§20-4)."
        ),
    },
    {
        "name": "media",
        "description": (
            "사진≤3장·영상 1개(≤200MB·≤3분). 영상 업로드=드래프트 생성+자막 시작(CAPTION-01), "
            "VIS-03 음성 입력. 한도: vision 20/일·5/분, caption 5/일 (게시물·채팅 합산)."
        ),
    },
    {"name": "friends", "description": "친구 요청·수락·거절·취소·해제 (FRIEND-01/02). 거절 후 30일 추천 제외."},
    {"name": "blocks", "description": "차단 (BLOCK-01) — 게시물·프로필·요청·채팅·추천 상호 제거."},
    {
        "name": "chat",
        "description": (
            "1:1 채팅 (CHAT-01~03) + AI 안심 채팅 (SAFE-01~05). 텍스트는 동기 분석 후 전달, "
            "주의는 수신자 블러+내용 보기. 3일 3회 누적 시 관계 단위 전송 제한(수신자 해제=리셋). "
            "사진·동영상은 분석 없이 즉시 전달, 미성년-성인 채팅은 텍스트만(§4.5)."
        ),
    },
    {"name": "ws", "description": "WS /api/v1/ws?token=<access> — 새 메시지·알림 실시간 푸시 (Redis pub/sub)."},
    {"name": "notifications", "description": "§16 알림 목록·읽음. 생성 시 WS 푸시 병행."},
    {
        "name": "recommendations",
        "description": "맞춤 친구 추천 (MATCH). 제외 규칙은 백엔드 강제, 점수·사유는 match-model. 모드·장애 비노출(MATCH-04).",
    },
    {
        "name": "comm",
        "description": "AI 소통 코치 (COMM-01~05). 버튼 실행 시에만 최근 10개 메시지를 외부 LLM에 전달(§17.2 고지).",
    },
]

description = """
**ThisAbled** — 장애 유형별 적응형 UI 소셜 플랫폼 백엔드 API (기능명세서 v2.1 정합).

### 인증 흐름
1. `GET /api/v1/auth/{provider}/authorize` → 제공자 로그인 → `GET /api/v1/auth/{provider}/callback` → `FRONTEND_URL`로 302
2. 기가입자: `?access_token=…` 쿼리로 즉시 발급 / 신규: `?signup_token=…`으로 `POST /api/v1/auth/signup`
3. 보호된 엔드포인트는 `Authorization: Bearer <access_token>` 헤더 필수.
4. access 만료(24h) 시 `POST /api/v1/auth/refresh` (httpOnly 쿠키 자동 전송).

### 공통 규칙
- 모든 경로 prefix: `/api/v1`
- 에러 응답 형식: `{ "detail": "<사람이 읽는 메시지>" }`
- 인증 누락·실패: `401` / 권한 없음: `403` / 검증 실패: `422`
- 차단·연령 정책 거부는 사유 비노출 `404`, SAFE-05 제한은 `403 "메시지를 보낼 수 없습니다"`
- 시간은 UTC ISO-8601, ID는 모두 UUID.
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    # 24h 드래프트 청소 등 인프로세스 크론 (테스트는 lifespan 미실행이라 영향 없음)
    from app.services.scheduler import start_scheduler, stop_scheduler

    start_scheduler()
    yield
    stop_scheduler()


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
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(media.router, prefix="/api/v1")
app.include_router(friends.router, prefix="/api/v1")
app.include_router(blocks.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(ws.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(recommendations.router, prefix="/api/v1")
app.include_router(comm.router, prefix="/api/v1")
