# Graph Report - thisabled-backend  (2026-07-06)

## Corpus Check
- 68 files · ~27,675 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 711 nodes · 1257 edges · 78 communities (56 shown, 22 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.75)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0877ad9e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Auth Test Suite|Auth Test Suite]]
- [[_COMMUNITY_Auth Endpoints & JWT Security|Auth Endpoints & JWT Security]]
- [[_COMMUNITY_App Core, Upload & Config|App Core, Upload & Config]]
- [[_COMMUNITY_Posts API & DB Models|Posts API & DB Models]]
- [[_COMMUNITY_GPT-4o Vision + Redis Cache|GPT-4o Vision + Redis Cache]]
- [[_COMMUNITY_Infra & Deployment Policy|Infra & Deployment Policy]]
- [[_COMMUNITY_User Disability-Mode Settings|User Disability-Mode Settings]]
- [[_COMMUNITY_Dev Workflow & Ralph Loop|Dev Workflow & Ralph Loop]]
- [[_COMMUNITY_Whisper STT Service|Whisper STT Service]]
- [[_COMMUNITY_get_redis|get_redis]]
- [[_COMMUNITY_Schema v2 Migration|Schema v2 Migration]]
- [[_COMMUNITY_Project Concept|Project Concept]]
- [[_COMMUNITY_Feature Branch Workflow|Feature Branch Workflow]]
- [[_COMMUNITY_Repository Root|Repository Root]]
- [[_COMMUNITY_MATCH-02 추천 입력|MATCH-02 추천 입력]]
- [[_COMMUNITY_예시 게시글 수정 API (PUT posts{id})|[예시] 게시글 수정 API (PUT /posts/{id})]]
- [[_COMMUNITY_ThisAbled 기능 명세서 v2.1|ThisAbled 기능 명세서 v2.1]]
- [[_COMMUNITY_14. 발달장애인 모드 및 AI 소통 코치|14. 발달장애인 모드 및 AI 소통 코치]]
- [[_COMMUNITY_7. 피드·게시물·댓글|7. 피드·게시물·댓글]]
- [[_COMMUNITY_11. AI 안심 채팅|11. AI 안심 채팅]]
- [[_COMMUNITY_1. 서비스 개요|1. 서비스 개요]]
- [[_COMMUNITY_4. 사용자 정책|4. 사용자 정책]]
- [[_COMMUNITY_env.py|env.py]]
- [[_COMMUNITY_12. 시각장애인 모드|12. 시각장애인 모드]]
- [[_COMMUNITY_17. 외부 AI 사용 및 데이터 처리 원칙|17. 외부 AI 사용 및 데이터 처리 원칙]]
- [[_COMMUNITY_6. 회원가입 및 계정|6. 회원가입 및 계정]]
- [[_COMMUNITY_10. 11 채팅|10. 1:1 채팅]]
- [[_COMMUNITY_13. 청각장애인 모드|13. 청각장애인 모드]]
- [[_COMMUNITY_18. 기술 구성|18. 기술 구성]]
- [[_COMMUNITY_19. 비기능 요구사항|19. 비기능 요구사항]]
- [[_COMMUNITY_9. 친구·차단|9. 친구·차단]]
- [[_COMMUNITY_3. MVP 범위|3. MVP 범위]]
- [[_COMMUNITY_5. 공통 화면 구조|5. 공통 화면 구조]]
- [[_COMMUNITY_Funnel 고정 URL|Funnel 고정 URL]]
- [[_COMMUNITY_Tailscale Funnel 임시 배포 가이드|Tailscale Funnel 임시 배포 가이드]]
- [[_COMMUNITY_CORS 오리진 명시 설정|CORS 오리진 명시 설정]]
- [[_COMMUNITY_Cloudflare Tunnel 임시 배포 가이드|Cloudflare Tunnel 임시 배포 가이드]]
- [[_COMMUNITY_refresh 쿠키 SameSite=None; Secure (크로스오리진)|refresh 쿠키 SameSite=None; Secure (크로스오리진)]]
- [[_COMMUNITY_예시 태스크 게시글 수정 API (PUT posts{id})|예시 태스크: 게시글 수정 API (PUT /posts/{id})]]
- [[_COMMUNITY_Ralph 루프 태스크 가이드|Ralph 루프 태스크 가이드]]
- [[_COMMUNITY_--max-iterations 필수 안전장치|--max-iterations 필수 안전장치]]
- [[_COMMUNITY_pytest 그린 = 완료 판정 기준|pytest 그린 = 완료 판정 기준]]
- [[_COMMUNITY_relations.py|relations.py]]
- [[_COMMUNITY_storage.py|storage.py]]
- [[_COMMUNITY_5. 공통 화면 구조|5. 공통 화면 구조]]
- [[_COMMUNITY_stt.py|stt.py]]
- [[_COMMUNITY_AsyncSession|AsyncSession]]
- [[_COMMUNITY_UploadFile|UploadFile]]
- [[_COMMUNITY_UploadFile|UploadFile]]
- [[_COMMUNITY_vision.py|vision.py]]
- [[_COMMUNITY_Redis|Redis]]
- [[_COMMUNITY_storage.py|storage.py]]
- [[_COMMUNITY_GoogleProvider|GoogleProvider]]
- [[_COMMUNITY_str|str]]
- [[_COMMUNITY_env.py|env.py]]
- [[_COMMUNITY_test_quota.py|test_quota.py]]
- [[_COMMUNITY_test_age.py|test_age.py]]
- [[_COMMUNITY_friends.py|friends.py]]
- [[_COMMUNITY_GoogleProvider|GoogleProvider]]
- [[_COMMUNITY_0. 문서 정보|0. 문서 정보]]
- [[_COMMUNITY_conftest.py|conftest.py]]
- [[_COMMUNITY_security.py|security.py]]
- [[_COMMUNITY_post.py|post.py]]
- [[_COMMUNITY_test_friends.py|test_friends.py]]
- [[_COMMUNITY_user.py|user.py]]
- [[_COMMUNITY_env.py|env.py]]
- [[_COMMUNITY_social.py|social.py]]
- [[_COMMUNITY_nickname.py|nickname.py]]
- [[_COMMUNITY_KakaoProvider|KakaoProvider]]
- [[_COMMUNITY_MockProvider|MockProvider]]

## God Nodes (most connected - your core abstractions)
1. `ThisAbled 기능 명세서 v2.1` - 23 edges
2. `Global Constraints` - 18 edges
3. `register()` - 17 edges
4. `_get_visible_post()` - 13 edges
5. `auth_header()` - 13 edges
6. `ThisAbled — Backend` - 12 edges
7. `_serialize_posts()` - 11 edges
8. `_request_out()` - 10 edges
9. `upload_video()` - 10 edges
10. `create_post()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `describe_post_media_job()` --indirect_call--> `db()`  [INFERRED]
  app/services/ai_media.py → tests/conftest.py
- `caption_post_media_job()` --indirect_call--> `db()`  [INFERRED]
  app/services/ai_media.py → tests/conftest.py
- `test_try_consume_respects_limit()` --calls--> `try_consume()`  [EXTRACTED]
  tests/test_quota.py → app/services/quota.py
- `test_cleanup_deletes_stale_drafts()` --calls--> `cleanup_stale_drafts()`  [EXTRACTED]
  tests/test_media.py → app/services/scheduler.py
- `test_full_age_boundaries()` --calls--> `full_age()`  [EXTRACTED]
  tests/test_age.py → app/core/age.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Docker Compose 스택 서비스 구성** — docker_compose_app, docker_compose_db, docker_compose_redis [EXTRACTED 0.90]

## Communities (78 total, 22 thin omitted)

### Community 0 - "Auth Test Suite"
Cohesion: 0.10
Nodes (33): cleanup_stale_drafts(), CAPTION-01: 업로드 후 24시간 미게시 내부 드래프트를 영상·자막과 함께 삭제.      이미 성공한 자막 생성의 일일 횟수 차감은 복, AsyncClient, auth_header(), client(), mock OAuth 가입 헬퍼 → {access_token, user_id, ...}., register(), ACC-01/02 — 소셜 OAuth 전용 인증 (mock 제공자). (+25 more)

### Community 1 - "Auth Endpoints & JWT Security"
Cohesion: 0.10
Nodes (44): me(), _me_out(), patch_me(), patch_settings(), public_profile(), put_mode(), put_tags(), AsyncSession (+36 more)

### Community 2 - "App Core, Upload & Config"
Cohesion: 0.22
Nodes (17): authorize(), callback(), logout(), AsyncSession, ACC-01/02 — 소셜 OAuth 전용 인증.  흐름: authorize → 제공자 로그인 → callback   - 기가입자: 즉시 로그인, refresh(), _set_refresh_cookie(), signup() (+9 more)

### Community 3 - "Posts API & DB Models"
Cohesion: 0.12
Nodes (23): ChatMessage, ChatRoom, 1:1 채팅방 (CHAT-01/02). request=요청함, active=일반 채팅.      참여자는 정규화 쌍(user_a < user_b, 채팅 메시지 (SAFE-01~03). 텍스트는 동기 분석 후 저장·전달., SAFE-05 관계 단위 자동 전송 제한.      누적 카운터는 별도 컬럼 없이 chat_messages에서     `flagged AND c, SendRestriction, AiResultCache, Notification (+15 more)

### Community 4 - "GPT-4o Vision + Redis Cache"
Cohesion: 0.13
Nodes (14): 0. 확정된 결정, 1. DB 스키마 v3 (baseline), 2. 아키텍처, 3. API 표면 (v1), 4. 문서 산출물, 5. 테스트 전략, 6. 구현 순서 (빅뱅), 7. 명세와의 정합 노트 (구현 설계에서 확정한 값) (+6 more)

### Community 5 - "Infra & Deployment Policy"
Cohesion: 0.50
Nodes (5): app 서비스 (FastAPI), db 서비스 (PostgreSQL 15), db/redis 호스트 포트 미노출 (내부 네트워크), app 루프백 바인딩 (127.0.0.1:8000), redis 서비스 (Redis 7)

### Community 6 - "User Disability-Mode Settings"
Cohesion: 0.09
Nodes (29): AiStatus, MediaType, MessageType, PostStatus, Provider, v2.1 도메인 enum. DB에는 String으로 저장한다 (PG enum 마이그레이션 부담 회피)., §POST-01 — '작성 중'은 서버 레코드 이전 단계라 상태로 두지 않음., description_status / caption_status 공용. (+21 more)

### Community 8 - "Whisper STT Service"
Cohesion: 0.10
Nodes (20): Global Constraints, Task 10: friends & blocks, Task 11: chat REST + SAFE 동기 파이프라인 + SAFE-05, Task 12: WebSocket + Redis pub/sub, Task 13: notifications, Task 14: recommendations + comm (모델 서버·LLM stub 경계), Task 15: mock 모델 서버 2종 + compose 배선, Task 16: 정리·전체 그린·문서 최종 정합 (+12 more)

### Community 9 - "get_redis"
Cohesion: 0.07
Nodes (27): 0. 사전 점검, 1) refresh 쿠키 SameSite — 이미 반영됨 ✅, 1. Tailscale 설치 & 로그인, 2) `.env` 설정, 2. Funnel 기능 켜기 (최초 1회, 콘솔에서), 3. Funnel 실행, 3) 프론트 fetch, Cloudflare Tunnel과 비교 (+19 more)

### Community 10 - "Schema v2 Migration"
Cohesion: 0.16
Nodes (18): async_sessionmaker, AsyncSession, BackgroundTasks, Redis, User, 미디어 업로드 — 사진(≤3장) · 영상(드래프트+자막 시작) · VIS-03 음성 입력., VIS-03 음성 입력 — 결과는 입력란 삽입용. 자동 게시하지 않는다 (§20-4)., 사진 업로드 (post 미연결) — POST /posts 의 media_ids로 연결한다. (+10 more)

### Community 11 - "Project Concept"
Cohesion: 0.15
Nodes (12): DB 스키마 (v3), graphify, Ralph 루프 (선택), ThisAbled — Backend, 기술 스택, 데드라인, 링크, 명령어 (+4 more)

### Community 21 - "MATCH-02 추천 입력"
Cohesion: 0.15
Nodes (13): 8. AI 사용자 매칭, MATCH-01 추천 목적, MATCH-02-1 자기소개, MATCH-02-2 관심사 태그, MATCH-02-3 사용자의 작성물, MATCH-02-4 분석 제외 데이터, MATCH-02-5 연령 정보, MATCH-02-6 좋아요 기반 관심 신호 (+5 more)

### Community 22 - "[예시] 게시글 수정 API (PUT /posts/{id})"
Cohesion: 0.17
Nodes (10): Definition of Done (체크리스트), 구현 범위, 배경 / 명세 출처, [예시] 게시글 수정 API (PUT /posts/{id}), 제약, Ralph 루프 태스크, 실행 방법, 안전장치 (필수) (+2 more)

### Community 23 - "ThisAbled 기능 명세서 v2.1"
Cohesion: 0.20
Nodes (9): 15. 마이페이지·설정, 16. 알림, 20. 핵심 인수 조건, 21. MVP 이후 계획, 2. 핵심 기능명, 3.1 포함, 3.2 제외 및 후속 범위, 3. MVP 범위 (+1 more)

### Community 24 - "14. 발달장애인 모드 및 AI 소통 코치"
Cohesion: 0.29
Nodes (7): 14. 발달장애인 모드 및 AI 소통 코치, COMM-01 쉬운 문장 변환, COMM-02 문장 완성, COMM-03 댓글·답장 추천, COMM-04 대화 힌트, COMM-05 데이터 처리 원칙, DEV-01 기본 UI

### Community 25 - "7. 피드·게시물·댓글"
Cohesion: 0.29
Nodes (7): 7. 피드·게시물·댓글, CAPTION-01 영상 자동 자막, FEED-01 홈 피드, POST-01 게시물 작성, POST-02 수정·삭제, POST-03 좋아요·댓글, VISION-01 AI 사진 설명

### Community 26 - "11. AI 안심 채팅"
Cohesion: 0.33
Nodes (6): 11. AI 안심 채팅, SAFE-01 분석 원칙과 전달 타이밍, SAFE-02 탐지 범위, SAFE-03 사용자 표시, SAFE-04 내부 위험 점수, SAFE-05 관계 단위 자동 전송 제한 (신설)

### Community 27 - "1. 서비스 개요"
Cohesion: 0.33
Nodes (6): 1.1 서비스명, 1.2 서비스 정의 (한 문장), 1.3 서비스 비전, 1.4 해결하려는 문제, 1.5 핵심 사용자 경험, 1. 서비스 개요

### Community 28 - "4. 사용자 정책"
Cohesion: 0.33
Nodes (6): 4.1 가입 대상, 4.2 장애인 자격 확인, 4.3 복합장애, 4.4 콘텐츠 공개, 4.5 미성년자 보호 (신설), 4. 사용자 정책

### Community 29 - "env.py"
Cohesion: 0.33
Nodes (3): 스키마 v3 baseline 정합 검증 (설계: docs/superpowers/specs/2026-07-05-v2_1-refactor-desig, 탈퇴 익명화(§15): 게시물·댓글·채팅 발신자는 SET NULL 가능해야 한다., test_anonymizable_fks_nullable()

### Community 30 - "12. 시각장애인 모드"
Cohesion: 0.40
Nodes (5): 12. 시각장애인 모드, VIS-01 기본 UI, VIS-02 스크린리더, VIS-03 음성 입력, VIS-04 상태 안내

### Community 31 - "17. 외부 AI 사용 및 데이터 처리 원칙"
Cohesion: 0.40
Nodes (5): 17.1 자체 처리 (외부 미전송), 17.2 외부 AI API 사용 (가입 시 필수 고지), 17.3 공통 처리 원칙, 17.4 관리자 기능, 17. 외부 AI 사용 및 데이터 처리 원칙

### Community 32 - "6. 회원가입 및 계정"
Cohesion: 0.40
Nodes (5): 6. 회원가입 및 계정, ACC-01 회원가입 (소셜 로그인), ACC-02 로그인·로그아웃, ACC-03 프로필, TAG-01 관심사 태그 체계 (정본)

### Community 33 - "10. 1:1 채팅"
Cohesion: 0.50
Nodes (4): 10. 1:1 채팅, CHAT-01 친구 채팅, CHAT-02 비친구 메시지 요청, CHAT-03 채팅 상태

### Community 34 - "13. 청각장애인 모드"
Cohesion: 0.50
Nodes (4): 13. 청각장애인 모드, HEAR-01 기본 UI, HEAR-02 영상 자막, HEAR-03 알림

### Community 35 - "18. 기술 구성"
Cohesion: 0.50
Nodes (4): 18.1 웹 서비스, 18.2 AI 모듈, 18.3 설계 원칙, 18. 기술 구성

### Community 36 - "19. 비기능 요구사항"
Cohesion: 0.50
Nodes (4): 19.1 접근성, 19.2 개인정보·보안, 19.3 AI 품질, 19. 비기능 요구사항

### Community 37 - "9. 친구·차단"
Cohesion: 0.50
Nodes (4): 9. 친구·차단, BLOCK-01 사용자 차단, FRIEND-01 친구 요청, FRIEND-02 친구 관리

### Community 38 - "3. MVP 범위"
Cohesion: 0.19
Nodes (6): Settings, lifespan(), 소셜 OAuth 제공자 추상화 (ACC-01).  - dev: OAUTH_MOCK=true → 모든 제공자 이름이 MockProvider로 동작, BaseSettings, FastAPI, v2.1 명세 고정값이 Settings에 반영되어 있는지 검증.

### Community 39 - "5. 공통 화면 구조"
Cohesion: 0.13
Nodes (41): _author_out(), _blocked_ids_subq(), caption_status(), _comment_out(), create_comment(), create_post(), delete_comment(), delete_post() (+33 more)

### Community 49 - "relations.py"
Cohesion: 0.33
Nodes (9): _post(), FEED-01 피드 · POST-01~03 게시물·댓글·좋아요., test_blocked_users_posts_hidden_both_ways(), test_comment_crud_and_count(), test_edit_delete_requires_author(), test_feed_cursor_pagination(), test_like_is_idempotent(), test_processing_draft_excluded_from_feed() (+1 more)

### Community 50 - "storage.py"
Cohesion: 0.18
Nodes (10): auth (ACC-01/02), chat (CHAT-01~03 · SAFE-01~05), comm (COMM-01~05), friends / blocks (FRIEND-01/02 · BLOCK-01), media (VISION-01 · CAPTION-01 · VIS-03), notifications (§16) / ws, posts / feed (FEED-01 · POST-01~03), recommendations (MATCH) (+2 more)

### Community 52 - "5. 공통 화면 구조"
Cohesion: 0.67
Nodes (3): 5.1 주요 화면, 5.2 UI 모드 전환, 5. 공통 화면 구조

### Community 53 - "stt.py"
Cohesion: 0.32
Nodes (7): _get_client(), OpenAI Whisper STT 서비스 (F02_S05 음성 댓글 / 자막).  엔드포인트는 `stt.transcribe(...)` 를 호출한, 오디오 바이트 → 한국어 전사 텍스트. (실제 Whisper 호출, VIS-03 음성 입력), 영상/오디오 → 자막 세그먼트 [{start, end, text}] (CAPTION-01)., transcribe(), transcribe_segments(), AsyncOpenAI

### Community 57 - "vision.py"
Cohesion: 0.08
Nodes (34): _ext_from_content_type(), Save file locally and return the public URL path., save_upload(), _cache_get(), _cache_put(), caption_post_media_job(), consume_vision(), describe_image() (+26 more)

### Community 63 - "test_quota.py"
Cohesion: 0.18
Nodes (16): caption_key(), _minute(), Redis TTL 카운터 — VISION-01·CAPTION-01 사용자별 호출 한도.  키는 날짜/분 단위로 자연 만료(TTL)되고, 자막 실, 카운터 1 증가. 한도 초과면 롤백 후 False., CAPTION-01: 자막 생성 실패(재시도 소진) 시 일일 횟수 차감 복원., 이미지 1장 = 1회, 게시물·채팅 합산 (VISION-01). [(키, 한도, TTL), ...], 영상 업로드 = 1회 차감, 게시물·채팅 합산 (CAPTION-01)., refund() (+8 more)

### Community 64 - "test_age.py"
Cohesion: 0.15
Nodes (20): age_band(), full_age(), is_minor(), 만 나이 계산 (§4.5 미성년 보호, MATCH-02-5 연령대).  생년월일 원문은 저장만 하고 파생값(만 나이·연령대·미성년)은 항상 요청, 만 14~18세 미성년 보호 대상 여부 (§4.5). 만 13 이하는 가입 자체가 불가., MATCH-02-5 연령대. 추천 특성으로만 사용, 생년월일 원문은 모델에 전달하지 않는다., normalize_pair(), 사용자 쌍 정규화. friendships·chat_rooms는 (작은 UUID, 큰 UUID) 순으로 저장한다. (+12 more)

### Community 65 - "friends.py"
Cohesion: 0.16
Nodes (29): create_block(), list_blocks(), AsyncSession, User, UUID, BLOCK-01 사용자 차단 — 게시물·프로필·요청·채팅·추천 상호 제거., remove_block(), accept_request() (+21 more)

### Community 66 - "GoogleProvider"
Cohesion: 0.14
Nodes (5): GoogleProvider, OAuthProvider, OAuthUserInfo, 구글 OAuth 2.0. 실검증은 키 발급 후., Protocol

### Community 67 - "0. 문서 정보"
Cohesion: 0.67
Nodes (3): 0.1 v2.1 주요 개정 사항, 0.2 v2.0 주요 개정 사항 (이력), 0. 문서 정보

### Community 68 - "conftest.py"
Cohesion: 0.21
Nodes (9): get_redis(), get_redis_client(), Redis, FastAPI 의존성. 테스트에서 override 가능하도록 분리., get_session_factory(), 백그라운드 작업(자막·설명 부착)용 세션 팩토리. 테스트에서 override., 테스트 공용 픽스처.  각 테스트는 단일 커넥션 위의 외부 트랜잭션에서 실행되고 끝나면 롤백된다. 앱 코드가 `await db.commit()`, test_redis() (+1 more)

### Community 69 - "security.py"
Cohesion: 0.31
Nodes (10): create_access_token(), create_refresh_token(), create_signup_token(), decode_signup_token(), decode_token(), _encode(), JWT 토큰 (access/refresh/signup). 소셜 OAuth 전용이라 비밀번호 해시는 없다 (ACC-01)., 콜백에서 신규 사용자에게 발급 — 추가 정보 입력(signup) 완료까지의 단기 자격. (+2 more)

### Community 70 - "post.py"
Cohesion: 0.20
Nodes (8): Comment, Post, PostLike, PostMedia, 게시물 (POST-01). 텍스트·사진=즉시 published, 영상=processing 드래프트로 시작., 게시물 미디어 (사진≤3·영상 1개는 앱 검증). VISION 설명·CAPTION 자막 부착., 좋아요 (POST-03). 멱등 토글, MATCH-02-6 관심 신호 입력., §15 회원 탈퇴.  - 계정·프로필 즉시 삭제 (users hard delete) - 게시물·댓글: 사용자가 익명화/삭제 선택 - 채팅 메시지

### Community 71 - "test_friends.py"
Cohesion: 0.44
Nodes (9): _pair(), FRIEND-01/02 친구 요청·관리 · BLOCK-01 차단., _request(), test_block_removes_friendship_and_hides_everything(), test_cancel_only_by_sender(), test_decline_records_and_duplicate_pending_rejected(), test_request_accept_creates_mutual_friendship(), test_self_request_rejected() (+1 more)

### Community 72 - "user.py"
Cohesion: 0.33
Nodes (6): get_current_user(), AsyncSession, get_db(), 서비스 사용자 (ACC-01). 만 나이·연령대·미성년 여부는 저장하지 않고 birth_date로 계산., User, HTTPAuthorizationCredentials

### Community 73 - "env.py"
Cohesion: 0.38
Nodes (5): do_run_migrations(), run_async_migrations(), run_migrations_online(), Base, DeclarativeBase

### Community 74 - "social.py"
Cohesion: 0.29
Nodes (6): Block, FriendRequest, Friendship, 친구 요청 (FRIEND-01). declined+responded_at → 30일 추천 제외(MATCH-03)., 양방향 친구 관계 (FRIEND-02). 정규화 쌍: user_a < user_b., 차단 (BLOCK-01). 게시물·프로필·요청·채팅·추천 접점을 상호 제거.

### Community 75 - "nickname.py"
Cohesion: 0.40
Nodes (4): AsyncSession, 닉네임 정책 (ACC-01): 2~12자 한글·영문·숫자, 금칙어·중복 불가., 형식(400) → 금칙어(400) → 중복(409) 순 검증. 통과 시 None., validate_nickname()

## Knowledge Gaps
- **163 isolated node(s):** `thisabled-backend`, `auth (ACC-01/02)`, `users (ACC-03 · TAG-01 · §15)`, `posts / feed (FEED-01 · POST-01~03)`, `media (VISION-01 · CAPTION-01 · VIS-03)` (+158 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ThisAbled 기능 명세서 v2.1` connect `ThisAbled 기능 명세서 v2.1` to `6. 회원가입 및 계정`, `10. 1:1 채팅`, `13. 청각장애인 모드`, `0. 문서 정보`, `18. 기술 구성`, `19. 비기능 요구사항`, `9. 친구·차단`, `5. 공통 화면 구조`, `MATCH-02 추천 입력`, `14. 발달장애인 모드 및 AI 소통 코치`, `7. 피드·게시물·댓글`, `11. AI 안심 채팅`, `1. 서비스 개요`, `4. 사용자 정책`, `12. 시각장애인 모드`, `17. 외부 AI 사용 및 데이터 처리 원칙`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Why does `upload_video()` connect `Schema v2 Migration` to `5. 공통 화면 구조`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **What connects `BLOCK-01 사용자 차단 — 게시물·프로필·요청·채팅·추천 상호 제거.`, `FRIEND-01 친구 요청 · FRIEND-02 친구 관리.`, `FRIEND-01/02 친구 요청·관리 · BLOCK-01 차단.` to the rest of the system?**
  _269 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Auth Test Suite` be split into smaller, more focused modules?**
  _Cohesion score 0.10384068278805121 - nodes in this community are weakly interconnected._
- **Should `Auth Endpoints & JWT Security` be split into smaller, more focused modules?**
  _Cohesion score 0.10453283996299723 - nodes in this community are weakly interconnected._
- **Should `Posts API & DB Models` be split into smaller, more focused modules?**
  _Cohesion score 0.12307692307692308 - nodes in this community are weakly interconnected._
- **Should `GPT-4o Vision + Redis Cache` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._