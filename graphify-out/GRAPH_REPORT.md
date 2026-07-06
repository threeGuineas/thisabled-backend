# Graph Report - thisabled-backend  (2026-07-06)

## Corpus Check
- 86 files · ~34,091 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 935 nodes · 1760 edges · 73 communities (52 shown, 21 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 25 edges (avg confidence: 0.69)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7aa0062e`
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
- [[_COMMUNITY_test_ws.py|test_ws.py]]
- [[_COMMUNITY_0. 문서 정보|0. 문서 정보]]
- [[_COMMUNITY_stt.py|stt.py]]
- [[_COMMUNITY_nickname.py|nickname.py]]
- [[_COMMUNITY_test_comm.py|test_comm.py]]
- [[_COMMUNITY_test_friends.py|test_friends.py]]
- [[_COMMUNITY_recommendations.py|recommendations.py]]

## God Nodes (most connected - your core abstractions)
1. `ThisAbled 기능 명세서 v2.1` - 23 edges
2. `Global Constraints` - 18 edges
3. `register()` - 17 edges
4. `_get_visible_post()` - 13 edges
5. `send_text()` - 13 edges
6. `auth_header()` - 13 edges
7. `send_media()` - 12 edges
8. `ThisAbled — Backend` - 12 edges
9. `_serialize_posts()` - 11 edges
10. `SafetyUnavailable` - 11 edges

## Surprising Connections (you probably didn't know these)
- `comm()` --indirect_call--> `get_comm_client()`  [INFERRED]
  tests/test_comm.py → app/services/comm.py
- `match()` --indirect_call--> `get_match_client()`  [INFERRED]
  tests/test_match.py → app/services/match.py
- `test_chat_send_publishes_event()` --calls--> `user_channel()`  [EXTRACTED]
  tests/test_ws.py → app/services/events.py
- `FakeSafety` --uses--> `SafetyUnavailable`  [INFERRED]
  tests/test_chat.py → app/services/safety.py
- `safety()` --indirect_call--> `get_safety_client()`  [INFERRED]
  tests/test_chat.py → app/services/safety.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Docker Compose 스택 서비스 구성** — docker_compose_app, docker_compose_db, docker_compose_redis [EXTRACTED 0.90]

## Communities (73 total, 21 thin omitted)

### Community 0 - "Auth Test Suite"
Cohesion: 0.07
Nodes (40): cleanup_stale_drafts(), CAPTION-01: 업로드 후 24시간 미게시 내부 드래프트를 영상·자막과 함께 삭제.      이미 성공한 자막 생성의 일일 횟수 차감은 복, AsyncClient, auth_header(), client(), db(), 테스트 공용 픽스처.  각 테스트는 단일 커넥션 위의 외부 트랜잭션에서 실행되고 끝나면 롤백된다. 앱 코드가 `await db.commit()`, 테스트가 직접 DB를 만질 때 사용 — client와 같은 커넥션을 공유한다. (+32 more)

### Community 1 - "Auth Endpoints & JWT Security"
Cohesion: 0.15
Nodes (32): me(), _me_out(), patch_me(), patch_settings(), public_profile(), put_mode(), put_tags(), AsyncSession (+24 more)

### Community 2 - "App Core, Upload & Config"
Cohesion: 0.05
Nodes (44): authorize(), callback(), logout(), AsyncSession, ACC-01/02 — 소셜 OAuth 전용 인증.  흐름: authorize → 제공자 로그인 → callback   - 기가입자: 즉시 로그인, refresh(), _set_refresh_cookie(), signup() (+36 more)

### Community 3 - "Posts API & DB Models"
Cohesion: 0.06
Nodes (54): do_run_migrations(), run_async_migrations(), run_migrations_online(), list_notifications(), mark_read(), NotificationListOut, NotificationOut, AsyncSession (+46 more)

### Community 4 - "GPT-4o Vision + Redis Cache"
Cohesion: 0.13
Nodes (14): 0. 확정된 결정, 1. DB 스키마 v3 (baseline), 2. 아키텍처, 3. API 표면 (v1), 4. 문서 산출물, 5. 테스트 전략, 6. 구현 순서 (빅뱅), 7. 명세와의 정합 노트 (구현 설계에서 확정한 값) (+6 more)

### Community 5 - "Infra & Deployment Policy"
Cohesion: 0.50
Nodes (5): app 서비스 (FastAPI), db 서비스 (PostgreSQL 15), db/redis 호스트 포트 미노출 (내부 네트워크), app 루프백 바인딩 (127.0.0.1:8000), redis 서비스 (Redis 7)

### Community 6 - "User Disability-Mode Settings"
Cohesion: 0.15
Nodes (18): AiStatus, MediaType, MessageType, PostStatus, Provider, v2.1 도메인 enum. DB에는 String으로 저장한다 (PG enum 마이그레이션 부담 회피)., §POST-01 — '작성 중'은 서버 레코드 이전 단계라 상태로 두지 않음., description_status / caption_status 공용. (+10 more)

### Community 8 - "Whisper STT Service"
Cohesion: 0.10
Nodes (20): Global Constraints, Task 10: friends & blocks, Task 11: chat REST + SAFE 동기 파이프라인 + SAFE-05, Task 12: WebSocket + Redis pub/sub, Task 13: notifications, Task 14: recommendations + comm (모델 서버·LLM stub 경계), Task 15: mock 모델 서버 2종 + compose 배선, Task 16: 정리·전체 그린·문서 최종 정합 (+12 more)

### Community 9 - "get_redis"
Cohesion: 0.07
Nodes (27): 0. 사전 점검, 1) refresh 쿠키 SameSite — 이미 반영됨 ✅, 1. Tailscale 설치 & 로그인, 2) `.env` 설정, 2. Funnel 기능 켜기 (최초 1회, 콘솔에서), 3. Funnel 실행, 3) 프론트 fetch, Cloudflare Tunnel과 비교 (+19 more)

### Community 10 - "Schema v2 Migration"
Cohesion: 0.19
Nodes (23): accept_request(), _author(), cancel_request(), decline_request(), _get_pending(), list_friends(), list_requests(), AsyncSession (+15 more)

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
Cohesion: 0.06
Nodes (58): ChatRoom, 1:1 채팅방 (CHAT-01/02). request=요청함, active=일반 채팅.      참여자는 정규화 쌍(user_a < user_b, SAFE-05 관계 단위 자동 전송 제한.      누적 카운터는 별도 컬럼 없이 chat_messages에서     `flagged AND c, SendRestriction, ChatPolicyError, counterpart_id(), flagged_count_since_reset(), get_or_create_room() (+50 more)

### Community 39 - "5. 공통 화면 구조"
Cohesion: 0.14
Nodes (40): _author_out(), _blocked_ids_subq(), caption_status(), _comment_out(), create_comment(), create_post(), delete_comment(), delete_post() (+32 more)

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
Cohesion: 0.10
Nodes (27): async_sessionmaker, AsyncSession, BackgroundTasks, Redis, User, 미디어 업로드 — 사진(≤3장) · 영상(드래프트+자막 시작) · VIS-03 음성 입력., VIS-03 음성 입력 — 결과는 입력란 삽입용. 자동 게시하지 않는다 (§20-4)., 사진 업로드 (post 미연결) — POST /posts 의 media_ids로 연결한다. (+19 more)

### Community 54 - "AsyncSession"
Cohesion: 0.13
Nodes (17): Redis, WS /api/v1/ws?token=<access> — 새 메시지·알림 실시간 푸시.  인증은 JWT 검증만으로 처리(DB 미조회)해 연결 비용, _relay(), ws_endpoint(), get_redis(), get_redis_client(), Redis, FastAPI 의존성. 테스트에서 override 가능하도록 분리. (+9 more)

### Community 57 - "vision.py"
Cohesion: 0.07
Nodes (41): _cache_get(), _cache_put(), caption_chat_message_job(), caption_post_media_job(), consume_vision(), describe_chat_message_job(), describe_image(), describe_post_media_job() (+33 more)

### Community 60 - "GoogleProvider"
Cohesion: 0.15
Nodes (32): accept_request(), _author(), create_room(), _get_my_room(), list_messages(), list_requests(), list_rooms(), _message_out() (+24 more)

### Community 63 - "test_quota.py"
Cohesion: 0.18
Nodes (16): caption_key(), _minute(), Redis TTL 카운터 — VISION-01·CAPTION-01 사용자별 호출 한도.  키는 날짜/분 단위로 자연 만료(TTL)되고, 자막 실, 카운터 1 증가. 한도 초과면 롤백 후 False., CAPTION-01: 자막 생성 실패(재시도 소진) 시 일일 횟수 차감 복원., 이미지 1장 = 1회, 게시물·채팅 합산 (VISION-01). [(키, 한도, TTL), ...], 영상 업로드 = 1회 차감, 게시물·채팅 합산 (CAPTION-01)., refund() (+8 more)

### Community 64 - "test_age.py"
Cohesion: 0.15
Nodes (20): age_band(), full_age(), is_minor(), 만 나이 계산 (§4.5 미성년 보호, MATCH-02-5 연령대).  생년월일 원문은 저장만 하고 파생값(만 나이·연령대·미성년)은 항상 요청, 만 14~18세 미성년 보호 대상 여부 (§4.5). 만 13 이하는 가입 자체가 불가., MATCH-02-5 연령대. 추천 특성으로만 사용, 생년월일 원문은 모델에 전달하지 않는다., normalize_pair(), 사용자 쌍 정규화. friendships·chat_rooms는 (작은 UUID, 큰 UUID) 순으로 저장한다. (+12 more)

### Community 65 - "friends.py"
Cohesion: 0.06
Nodes (59): create_block(), list_blocks(), AsyncSession, User, UUID, BLOCK-01 사용자 차단 — 게시물·프로필·요청·채팅·추천 상호 제거., remove_block(), complete() (+51 more)

### Community 67 - "0. 문서 정보"
Cohesion: 0.67
Nodes (3): 0.1 v2.1 주요 개정 사항, 0.2 v2.0 주요 개정 사항 (이력), 0. 문서 정보

### Community 70 - "test_comm.py"
Cohesion: 0.09
Nodes (9): get_comm_client(), OpenAICommClient, COMM — LLM 소통 코치 (외부 API, §17.2 고지 대상).  버튼 실행 시에만 동작(COMM-05). 채팅 컨텍스트는 최근 N개 텍, 키 미설정 dev/시연용 — 고정 후보., FastAPI 의존성 — 테스트에서 fake로 override., StubCommClient, comm(), FakeComm (+1 more)

### Community 71 - "test_friends.py"
Cohesion: 0.44
Nodes (9): _pair(), FRIEND-01/02 친구 요청·관리 · BLOCK-01 차단., _request(), test_block_removes_friendship_and_hides_everything(), test_cancel_only_by_sender(), test_decline_records_and_duplicate_pending_rejected(), test_request_accept_creates_mutual_friendship(), test_self_request_rejected() (+1 more)

### Community 72 - "recommendations.py"
Cohesion: 0.12
Nodes (19): AsyncSession, User, RecommendationListOut, RecommendationOut, recommendations(), candidate_pool(), get_match_client(), MatchClient (+11 more)

## Knowledge Gaps
- **163 isolated node(s):** `thisabled-backend`, `auth (ACC-01/02)`, `users (ACC-03 · TAG-01 · §15)`, `posts / feed (FEED-01 · POST-01~03)`, `media (VISION-01 · CAPTION-01 · VIS-03)` (+158 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ThisAbled 기능 명세서 v2.1` connect `ThisAbled 기능 명세서 v2.1` to `6. 회원가입 및 계정`, `10. 1:1 채팅`, `13. 청각장애인 모드`, `0. 문서 정보`, `18. 기술 구성`, `19. 비기능 요구사항`, `9. 친구·차단`, `5. 공통 화면 구조`, `MATCH-02 추천 입력`, `14. 발달장애인 모드 및 AI 소통 코치`, `7. 피드·게시물·댓글`, `11. AI 안심 채팅`, `1. 서비스 개요`, `4. 사용자 정책`, `12. 시각장애인 모드`, `17. 외부 AI 사용 및 데이터 처리 원칙`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Why does `upload_video()` connect `stt.py` to `5. 공통 화면 구조`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **What connects `COMM-01~05 — AI 소통 코치. 전 모드 제공, 발달 모드 기본 노출(§14).`, `COMM-05: 참여자 검증 후 최근 N개 텍스트. flagged 미열람·pending은 제외.`, `COMM-02: 제안일 뿐, 자동 입력·게시하지 않는다 (§20-8).` to the rest of the system?**
  _309 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Auth Test Suite` be split into smaller, more focused modules?**
  _Cohesion score 0.06638714185883997 - nodes in this community are weakly interconnected._
- **Should `Auth Endpoints & JWT Security` be split into smaller, more focused modules?**
  _Cohesion score 0.14795008912655971 - nodes in this community are weakly interconnected._
- **Should `App Core, Upload & Config` be split into smaller, more focused modules?**
  _Cohesion score 0.05191146881287726 - nodes in this community are weakly interconnected._
- **Should `Posts API & DB Models` be split into smaller, more focused modules?**
  _Cohesion score 0.05874125874125874 - nodes in this community are weakly interconnected._