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
from app.openapi import install_openapi

# Swagger 사이드바 그룹 설명 — 프론트가 어떤 묶음을 봐야 하는지 한눈에.
# SSOT: docs/ThisAbled_기능명세서_v2_2.md / 요약: docs/api.md
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
**ThisAbled** — 장애 유형별 적응형 UI 소셜 플랫폼 백엔드 API입니다.
이 문서는 기능명세서 v2.2를 기준으로 프론트엔드가 별도 추측 없이 구현할 수 있도록 작성했습니다.

## 프론트엔드 빠른 시작

1. `GET /api/v1/auth/{provider}/authorize`의 URL로 브라우저를 이동합니다.
2. callback은 JSON이 아니라 `FRONTEND_URL`로 302 이동합니다.
   - 기존 회원: `?is_new_user=false&access_token=...`
   - 신규 회원: `?is_new_user=true&signup_token=...` → `POST /api/v1/auth/signup`
   - 로그인 실패·거부: `?error={provider}_failed`
3. 보호된 API에는 `Authorization: Bearer <access_token>`을 보냅니다.
4. access token 만료로 401을 받으면 `POST /api/v1/auth/refresh`를 **한 번만** 호출한 뒤 원 요청을 재시도합니다.
   refresh/logout 요청은 httpOnly 쿠키를 사용하므로 브라우저 fetch의 `credentials: "include"`가 필요합니다.
5. 앱 시작 시 `GET /users/me`로 모드·프로필·설정을 서버 정본과 동기화합니다.

## 응답과 오류 처리

- 모든 REST 경로 prefix는 `/api/v1`, ID는 UUID, 날짜·시간은 UTC ISO-8601입니다.
- 일반 정책 오류는 `{ "detail": "사람이 읽는 메시지" }`입니다.
- FastAPI 형식 검증 422는 `{ "detail": [{ "loc": [...], "msg": "...", "type": "..." }] }` 배열입니다.
- 401은 토큰 재발급 대상으로 처리하고, 403은 권한·정책 거부, 404는 실제 없음뿐 아니라 차단·보호 정책상
  존재를 숨긴 경우도 포함합니다. 404 사유를 화면에서 추정하거나 구분하지 마세요.
- 모든 비동기 요청은 성공·오류·빈 배열 여부와 관계없이 finally에서 로딩 상태를 해제하세요.
- `204 No Content`는 JSON 파싱을 시도하지 않습니다.

## 목록과 미디어

- 피드·채팅 메시지는 서버가 발급한 불투명 `next_cursor`를 그대로 다음 요청에 전달합니다. null이면 마지막입니다.
- 사진 업로드 결과의 `media_id`는 `/posts`에 연결해야 공개됩니다.
- 영상 업로드는 `processing` 드래프트를 만들 뿐 자동 공개하지 않습니다. 자막 상태가 끝난 뒤 publish가 필요합니다.
- `/uploads/...` 상대 URL은 현재 API origin을 기준으로 절대 URL로 변환하세요.

## AI 기능의 화면 처리

- 추천 API는 후보 부족·MATCH 장애도 HTTP 200으로 반환합니다. `items=[]`이면 반드시 `message`를 표시하고 로딩을 끝냅니다.
- 소통 코치의 문장·후보는 JSON 코드블록이 아닌 평문입니다. 사용자가 선택하기 전 자동 입력·게시·전송하지 않습니다.
- AI 미디어 상태는 `none | processing | done | failed`입니다. failed를 무한 폴링하지 마세요.

## WebSocket (OpenAPI 비지원 영역)

- 연결: `wss://<현재 API 호스트>/api/v1/ws?token=<access_token>` (로컬은 `ws://localhost:8000`)
- 인증 실패 종료 코드: `4401`. access token을 재발급한 뒤 새 연결을 만드세요.
- 이벤트는 모두 `{ "type": "...", "payload": { ... } }` 형식입니다.
  - `chat.message`: `{room_id, message_id}` — 원문은 없으며 해당 방 REST 목록을 다시 조회합니다.
  - `chat.read`: `{room_id, message_id}` — 상대가 이 message_id까지 읽었습니다.
  - `notification`: `{type, ...도메인별 payload}` — 알림 목록을 다시 조회해 정본과 맞춥니다.
- 재연결은 지수 백오프를 사용하고, 같은 `message_id` 이벤트가 재수신돼도 중복 삽입하지 마세요.
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
    version="0.3.0",
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

# 모든 라우터가 등록된 뒤 메서드+경로별 상세 설명·예시·오류 계약을 주입한다.
install_openapi(app)
