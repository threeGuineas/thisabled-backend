# Graph Report - thisabled-backend  (2026-08-15)

## Corpus Check
- 112 files · ~52,783 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1148 nodes · 2624 edges · 123 communities (75 shown, 48 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 157 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `aa2c6a2e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/chat.py
- BaseModel
- User
- ai_media.py
- ai_result_cache 테이블(미디어 해시 캐싱)
- friends.py
- test_chat.py
- register
- Global Constraints
- v1/media.py
- 임시 배포 — 맥미니 로컬호스팅 + Tailscale Funnel
- ThisAbled 백엔드 v2.1 전면 리팩토링 — 설계
- test_ws.py
- oauth.py
- safe_grooming_eval.py
- 채팅 읽음 상태 설계
- ThisAbled API 명세 요약 (v2.2)
- MATCH-02 추천 입력
- test_auth.py
- match.py
- ThisAbled — Backend
- ThisAbled 기능 명세서 v2.2
- [예시] 게시글 수정 API (PUT /posts/{id})
- v1/auth.py
- 소셜 OAuth 실키 발급·투입·검증 가이드
- test_friends.py
- Global Constraints
- SAFE 그루밍 평가 설계
- 14. 발달장애인 모드 및 AI 소통 코치
- 7. 피드·게시물·댓글
- conftest.py
- 11. AI 안심 채팅
- 1. 서비스 개요
- test_media.py
- 4. 사용자 정책
- 10. 1:1 채팅
- 12. 시각장애인 모드
- config.py
- SAFE 이진 v6 배포 검증
- 17. 외부 AI 사용 및 데이터 처리 원칙
- 6. 회원가입 및 계정
- 0. 문서 정보
- v1/comm.py
- SAFE 최신 호환 서빙 재평가
- 13. 청각장애인 모드
- 18. 기술 구성
- 19. 비기능 요구사항
- 5. 공통 화면 구조
- 9. 친구·차단
- MATCH v2 배포 성능 평가
- friendships 테이블(정규화 쌍)
- WebSocket + Redis pub/sub 팬아웃
- withdrawn_socials 테이블
- _Redis
- test_schema.py
- SAFE 그루밍 평가 결과
- get_current_user
- ws.py
- Funnel 고정 URL
- Tailscale Funnel 임시 배포 가이드
- CORS 오리진 명시 설정
- Cloudflare Tunnel 임시 배포 가이드
- OpenAI 비용 노출 위험 (vision/stt)
- refresh 쿠키 SameSite=None; Secure (크로스오리진)
- 예시 태스크: 게시글 수정 API (PUT /posts/{id})
- Ralph 루프 태스크 가이드
- --max-iterations 필수 안전장치
- pytest 그린 = 완료 판정 기준
- forbidden_nicknames 테이블
- notifications 테이블
- social_identities 테이블
- user_interest_tags 테이블
- user_mode_history 테이블
- tools/__init__.py
- test_config.py
- blocks.py
- stt.py
- thisabled-backend
- test_notifications.py
- env.py
- withdraw
- 스키마 v3 baseline(빅뱅)
- 만나이·연령대 유틸(age.py)
- APScheduler 인프로세스 크론(24h 청소·재분석)
- blocks 테이블
- chat_messages 테이블(safety_status)
- chat_rooms 테이블(request|active)
- comments 테이블
- friend_requests 테이블
- interest_tags 테이블
- match-model HTTP 경계(SBERT+LightGBM, mock)
- OAuth mock 제공자(env 토글, 실키 교체)
- post_likes 테이블
- post_media 테이블
- posts 테이블
- safety-model HTTP 경계(자체 안전 모델, mock)
- send_restrictions 테이블(SAFE-05)
- signup_token(단기 가입 토큰, 30분)
- Google OAuth Setup
- Kakao OAuth Setup
- OAuth Mock Provider (dev)
- OAuth Redirect URI Decision
- Definition of Done 체크리스트
- Redis TTL 호출 한도 카운터(vision·caption)
- users 테이블
- Chat Read Status Implementation Plan
- Task 1 — Failing behavior tests
- Task 2 report — persistence and cursor helpers
- progress.md
- Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?
- Q: 백엔드 핵심 소스코드 2개와 설명
- task-1-brief.md
- task-2-brief.md

## God Nodes (most connected - your core abstractions)
1. `User` - 78 edges
2. `register()` - 70 edges
3. `auth_header()` - 66 edges
4. `Base` - 29 edges
5. `ChatMessage` - 26 edges
6. `ThisAbled 기능 명세서 v2.2` - 23 edges
7. `send_media()` - 21 edges
8. `ChatRoom` - 21 edges
9. `PostMedia` - 20 edges
10. `_room()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `reanalyze_unanalyzed()` --indirect_call--> `db()`  [INFERRED]
  app/services/chat.py → tests/conftest.py
- `test_photo_post_gets_description_on_publish()` --indirect_call--> `PostMedia`  [INFERRED]
  tests/test_media.py → app/models/post.py
- `test_vision_quota_exceeded_publishes_without_description()` --indirect_call--> `PostMedia`  [INFERRED]
  tests/test_media.py → app/models/post.py
- `test_cleanup_deletes_stale_drafts()` --indirect_call--> `Post`  [INFERRED]
  tests/test_media.py → app/models/post.py
- `test_withdraw_anonymize_keeps_posts_and_chat()` --indirect_call--> `ChatMessage`  [INFERRED]
  tests/test_withdrawal.py → app/models/chat.py

## Import Cycles
- None detected.

## Communities (123 total, 48 thin omitted)

### Community 0 - "v1/chat.py"
Cohesion: 0.07
Nodes (77): accept_request(), _author(), create_room(), _get_my_room(), list_messages(), list_requests(), list_rooms(), _message_out() (+69 more)

### Community 1 - "BaseModel"
Cohesion: 0.07
Nodes (57): me(), _me_out(), patch_me(), patch_settings(), public_profile(), put_mode(), put_tags(), AsyncSession (+49 more)

### Community 2 - "User"
Cohesion: 0.08
Nodes (71): UploadFile, VIS-03 음성 입력 — 결과는 입력란 삽입용. 자동 게시하지 않는다 (§20-4)., 사진 업로드 (post 미연결) — POST /posts 의 media_ids로 연결한다., transcribe_voice(), upload_images(), _author_out(), _blocked_ids_subq(), caption_status() (+63 more)

### Community 3 - "ai_media.py"
Cohesion: 0.05
Nodes (62): async_sessionmaker, AsyncSession, BackgroundTasks, Redis, 영상 첨부 = processing 내부 드래프트 생성 + 자막 생성 즉시 시작 (POST-01·CAPTION-01).      길이(≤3분)는, upload_video(), AiResultCache, 동일 미디어 해시 캐싱 (VISION-01·CAPTION-01 중복 호출 방지, 비용 방어). (+54 more)

### Community 5 - "friends.py"
Cohesion: 0.12
Nodes (38): accept_request(), _author(), cancel_request(), decline_request(), _get_pending(), list_friends(), list_requests(), AsyncSession (+30 more)

### Community 6 - "test_chat.py"
Cohesion: 0.17
Nodes (27): _describe_fake(), make_friends(), CHAT-01 친구 채팅 · CHAT-02 비친구 요청 · 미디어 제한 (§4.5)., _room(), _send(), test_friend_chat_roundtrip(), test_media_blocked_in_request_room(), test_media_only_between_adult_friends() (+19 more)

### Community 7 - "register"
Cohesion: 0.17
Nodes (27): Block, 차단 (BLOCK-01). 게시물·프로필·요청·채팅·추천 접점을 상호 제거., auth_header(), mock OAuth 가입 헬퍼 → {access_token, user_id, ...}., register(), MATCH — 후보 제외 규칙은 백엔드 강제, 점수·사유는 모델 서버 (mock/fake)., test_empty_pool_message(), test_exclusion_rules_enforced_by_backend() (+19 more)

### Community 8 - "Global Constraints"
Cohesion: 0.10
Nodes (20): Global Constraints, Task 10: friends & blocks, Task 11: chat REST + SAFE 동기 파이프라인 + SAFE-05, Task 12: WebSocket + Redis pub/sub, Task 13: notifications, Task 14: recommendations + comm (모델 서버·LLM stub 경계), Task 15: mock 모델 서버 2종 + compose 배선, Task 16: 정리·전체 그린·문서 최종 정합 (+12 more)

### Community 9 - "v1/media.py"
Cohesion: 0.16
Nodes (16): 미디어 업로드 — 사진(≤3장) · 영상(드래프트+자막 시작) · VIS-03 음성 입력., Base, get_db(), get_session_factory(), 백그라운드 작업(자막·설명 부착)용 세션 팩토리. 테스트에서 override., _utcnow(), Notification, 알림 (§16). WS 푸시와 병행 저장. (+8 more)

### Community 10 - "임시 배포 — 맥미니 로컬호스팅 + Tailscale Funnel"
Cohesion: 0.07
Nodes (27): 0. 사전 점검, 1) refresh 쿠키 SameSite — 이미 반영됨 ✅, 1. Tailscale 설치 & 로그인, 2) `.env` 설정, 2. Funnel 기능 켜기 (최초 1회, 콘솔에서), 3. Funnel 실행, 3) 프론트 fetch, Cloudflare Tunnel과 비교 (+19 more)

### Community 11 - "ThisAbled 백엔드 v2.1 전면 리팩토링 — 설계"
Cohesion: 0.13
Nodes (14): 0. 확정된 결정, 1. DB 스키마 v3 (baseline), 2. 아키텍처, 3. API 표면 (v1), 4. 문서 산출물, 5. 테스트 전략, 6. 구현 순서 (빅뱅), 7. 명세와의 정합 노트 (구현 설계에서 확정한 값) (+6 more)

### Community 12 - "test_ws.py"
Cohesion: 0.17
Nodes (13): user_channel(), get_safety_client(), FastAPI 의존성 — 테스트에서 fake로 override., FakeSafety, 돈' 포함 → flagged. fail=True → SafetyUnavailable (§18.3)., safety(), safety(), WS 푸시 — 토큰 검증, pub/sub 릴레이, 채팅 전송 이벤트. (+5 more)

### Community 13 - "oauth.py"
Cohesion: 0.09
Nodes (15): authorize(), AuthorizeOut, get_provider(), GoogleProvider, _http(), KakaoProvider, MockProvider, OAuthProvider (+7 more)

### Community 14 - "safe_grooming_eval.py"
Cohesion: 0.24
Nodes (16): Any, test_fixture_contains_detection_and_boundary_cases(), test_fixture_rows_match_case_schema(), test_invalid_case_is_rejected(), test_invalid_verdict_is_error_not_safe(), test_summarize_reports_recall_fnr_fpr_and_subgroups(), evaluate(), _group_metrics() (+8 more)

### Community 15 - "채팅 읽음 상태 설계"
Cohesion: 0.22
Nodes (8): API와 실시간 이벤트, 대안과 결정, 데이터 모델, 목표, 범위와 용어, 안전성과 일관성, 채팅 읽음 상태 설계, 테스트

### Community 16 - "ThisAbled API 명세 요약 (v2.2)"
Cohesion: 0.18
Nodes (10): auth (ACC-01/02), chat (CHAT-01~03 · SAFE-01~05), comm (COMM-01~05), friends / blocks (FRIEND-01/02 · BLOCK-01), media (VISION-01 · CAPTION-01 · VIS-03), notifications (§16) / ws, posts / feed (FEED-01 · POST-01~03), recommendations (MATCH) (+2 more)

### Community 17 - "MATCH-02 추천 입력"
Cohesion: 0.15
Nodes (13): 8. AI 사용자 매칭, MATCH-01 추천 목적, MATCH-02-1 자기소개, MATCH-02-2 관심사 태그, MATCH-02-3 사용자의 작성물, MATCH-02-4 분석 제외 데이터, MATCH-02-5 연령 정보, MATCH-02-6 좋아요 기반 관심 신호 (+5 more)

### Community 18 - "test_auth.py"
Cohesion: 0.10
Nodes (28): callback_params(), 콜백 302 리다이렉트(Location=FRONTEND_URL?…)의 쿼리 파라미터 → 단일값 dict., ACC-01/02 — 소셜 OAuth 전용 인증 (mock 제공자)., _signup_token(), test_callback_new_user_redirects_with_signup_token(), test_existing_user_callback_logs_in(), test_invalid_mock_code_redirects_with_error(), test_refresh_rotates_access_token() (+20 more)

### Community 19 - "match.py"
Cohesion: 0.11
Nodes (29): AsyncSession, RecommendationListOut, RecommendationOut, recommendations(), age_band(), full_age(), is_minor(), 만 나이 계산 (§4.5 미성년 보호, MATCH-02-5 연령대).  생년월일 원문은 저장만 하고 파생값(만 나이·연령대·미성년)은 항상 요청 (+21 more)

### Community 20 - "ThisAbled — Backend"
Cohesion: 0.15
Nodes (12): DB 스키마 (v3), graphify, Ralph 루프 (선택), ThisAbled — Backend, 기술 스택, 데드라인, 링크, 명령어 (+4 more)

### Community 21 - "ThisAbled 기능 명세서 v2.2"
Cohesion: 0.20
Nodes (9): 15. 마이페이지·설정, 16. 알림, 20. 핵심 인수 조건, 21. MVP 이후 계획, 2. 핵심 기능명, 3.1 포함, 3.2 제외 및 후속 범위, 3. MVP 범위 (+1 more)

### Community 22 - "[예시] 게시글 수정 API (PUT /posts/{id})"
Cohesion: 0.17
Nodes (10): Definition of Done (체크리스트), 구현 범위, 배경 / 명세 출처, [예시] 게시글 수정 API (PUT /posts/{id}), 제약, Ralph 루프 태스크, 실행 방법, 안전장치 (필수) (+2 more)

### Community 23 - "v1/auth.py"
Cohesion: 0.15
Nodes (28): callback(), _frontend_redirect(), logout(), AsyncSession, get, post, UUID, ACC-01/02 — 소셜 OAuth 전용 인증. 흐름: authorize → 제공자 로그인 → callback → FRONTEND_URL로… (+20 more)

### Community 24 - "소셜 OAuth 실키 발급·투입·검증 가이드"
Cohesion: 0.25
Nodes (7): 0. 사전 결정: redirect URI, 1. 카카오 (developers.kakao.com), 2. 구글 (console.cloud.google.com), 3. 환경변수 투입, 4. 실검증 체크리스트, 소셜 OAuth 실키 발급·투입·검증 가이드, 자주 걸리는 오류

### Community 25 - "test_friends.py"
Cohesion: 0.44
Nodes (9): _pair(), FRIEND-01/02 친구 요청·관리 · BLOCK-01 차단., _request(), test_block_removes_friendship_and_hides_everything(), test_cancel_only_by_sender(), test_decline_records_and_duplicate_pending_rejected(), test_request_accept_creates_mutual_friendship(), test_self_request_rejected() (+1 more)

### Community 26 - "Global Constraints"
Cohesion: 0.29
Nodes (6): Global Constraints, SAFE Grooming Evaluation Implementation Plan, Task 1: Add the evaluation fixture and pure metric tests, Task 2: Implement the pure evaluator and CLI, Task 3: Run the real SAFE evaluation, Task 4: Verify and document limitations

### Community 27 - "SAFE 그루밍 평가 설계"
Cohesion: 0.29
Nodes (6): SAFE 그루밍 평가 설계, 목적, 범위, 비범위, 성공 기준, 실행 흐름

### Community 28 - "14. 발달장애인 모드 및 AI 소통 코치"
Cohesion: 0.29
Nodes (7): 14. 발달장애인 모드 및 AI 소통 코치, COMM-01 쉬운 문장 변환, COMM-02 문장 완성, COMM-03 댓글·답장 추천, COMM-04 대화 힌트, COMM-05 데이터 처리 원칙, DEV-01 기본 UI

### Community 29 - "7. 피드·게시물·댓글"
Cohesion: 0.29
Nodes (7): 7. 피드·게시물·댓글, CAPTION-01 영상 자동 자막, FEED-01 홈 피드, POST-01 게시물 작성, POST-02 수정·삭제, POST-03 좋아요·댓글, VISION-01 AI 사진 설명

### Community 30 - "conftest.py"
Cohesion: 0.15
Nodes (15): async_sessionmaker, AsyncClient, _BorrowedSession, client(), _conn(), _force_oauth_mock(), AsyncClient, fixture (+7 more)

### Community 31 - "11. AI 안심 채팅"
Cohesion: 0.33
Nodes (6): 11. AI 안심 채팅, SAFE-01 분석 원칙과 전달 타이밍, SAFE-02 탐지 범위, SAFE-03 사용자 표시, SAFE-04 내부 위험 점수, SAFE-05 관계 단위 자동 전송 제한 (신설)

### Community 32 - "1. 서비스 개요"
Cohesion: 0.33
Nodes (6): 1.1 서비스명, 1.2 서비스 정의 (한 문장), 1.3 서비스 비전, 1.4 해결하려는 문제, 1.5 핵심 사용자 경험, 1. 서비스 개요

### Community 33 - "test_media.py"
Cohesion: 0.12
Nodes (20): cleanup_stale_drafts(), CAPTION-01: 업로드 후 24시간 미게시 내부 드래프트를 영상·자막과 함께 삭제.      이미 성공한 자막 생성의 일일 횟수 차감은 복, PostMedia, CallCounter, fake_ai(), fixture, VISION-01 사진 설명 · CAPTION-01 영상 자막 · VIS-03 음성 입력 · 24h 드래프트 청소., 외부 AI caller를 fake로 대체 — 실호출 금지 (Global Constraints). (+12 more)

### Community 34 - "4. 사용자 정책"
Cohesion: 0.33
Nodes (6): 4.1 가입 대상, 4.2 장애인 자격 확인, 4.3 복합장애, 4.4 콘텐츠 공개, 4.5 미성년자 보호 (신설), 4. 사용자 정책

### Community 35 - "10. 1:1 채팅"
Cohesion: 0.40
Nodes (5): 10. 1:1 채팅, CHAT-01 친구 채팅, CHAT-02 비친구 메시지 요청, CHAT-03 채팅 상태, CHAT-04 읽음·안읽음 표시 (신설)

### Community 36 - "12. 시각장애인 모드"
Cohesion: 0.40
Nodes (5): 12. 시각장애인 모드, VIS-01 기본 UI, VIS-02 스크린리더, VIS-03 음성 입력, VIS-04 상태 안내

### Community 37 - "config.py"
Cohesion: 0.22
Nodes (9): health(), get, lifespan(), COMM — LLM 소통 코치 (외부 API, §17.2 고지 대상).  버튼 실행 시에만 동작(COMM-05). 채팅 컨텍스트는 최근 N개 텍, APScheduler 인프로세스 크론 — 24h 드래프트 청소 (+ Task 11에서 미분석 재분석 추가)., start_scheduler(), stop_scheduler(), AsyncIOScheduler (+1 more)

### Community 38 - "SAFE 이진 v6 배포 검증"
Cohesion: 0.33
Nodes (5): FN, FP, SAFE 이진 v6 배포 검증, 백엔드 회귀 확인, 판정

### Community 39 - "17. 외부 AI 사용 및 데이터 처리 원칙"
Cohesion: 0.40
Nodes (5): 17.1 자체 처리 (외부 미전송), 17.2 외부 AI API 사용 (가입 시 필수 고지), 17.3 공통 처리 원칙, 17.4 관리자 기능, 17. 외부 AI 사용 및 데이터 처리 원칙

### Community 40 - "6. 회원가입 및 계정"
Cohesion: 0.40
Nodes (5): 6. 회원가입 및 계정, ACC-01 회원가입 (소셜 로그인), ACC-02 로그인·로그아웃, ACC-03 프로필, TAG-01 관심사 태그 체계 (정본)

### Community 41 - "0. 문서 정보"
Cohesion: 0.50
Nodes (4): 0.0 v2.2 주요 개정 사항, 0.1 v2.1 주요 개정 사항 (이력), 0.2 v2.0 주요 개정 사항 (이력), 0. 문서 정보

### Community 42 - "v1/comm.py"
Cohesion: 0.06
Nodes (35): complete(), hints(), HintsOut, AsyncSession, UUID, COMM-01~05 — AI 소통 코치. 전 모드 제공, 발달 모드 기본 노출(§14)., COMM-05: 참여자 검증 후 최근 N개 텍스트. flagged 미열람·pending은 제외., COMM-02: 제안일 뿐, 자동 입력·게시하지 않는다 (§20-8). (+27 more)

### Community 43 - "SAFE 최신 호환 서빙 재평가"
Cohesion: 0.40
Nodes (4): SAFE 최신 호환 서빙 재평가, 결과, 결론, 실행 기준

### Community 44 - "13. 청각장애인 모드"
Cohesion: 0.50
Nodes (4): 13. 청각장애인 모드, HEAR-01 기본 UI, HEAR-02 영상 자막, HEAR-03 알림

### Community 45 - "18. 기술 구성"
Cohesion: 0.50
Nodes (4): 18.1 웹 서비스, 18.2 AI 모듈, 18.3 설계 원칙, 18. 기술 구성

### Community 46 - "19. 비기능 요구사항"
Cohesion: 0.50
Nodes (4): 19.1 접근성, 19.2 개인정보·보안, 19.3 AI 품질, 19. 비기능 요구사항

### Community 47 - "5. 공통 화면 구조"
Cohesion: 0.50
Nodes (4): 5.1 주요 화면, 5.2 UI 모드 전환, 5.3 기본 모드 (GEN-01, 신설), 5. 공통 화면 구조

### Community 48 - "9. 친구·차단"
Cohesion: 0.50
Nodes (4): 9. 친구·차단, BLOCK-01 사용자 차단, FRIEND-01 친구 요청, FRIEND-02 친구 관리

### Community 50 - "MATCH v2 배포 성능 평가"
Cohesion: 0.20
Nodes (9): 1. 기동 및 계약, 2.1 배포 번들 저장 지표, 2.2 배포 모델 독립 재평가, 2. 랭킹 품질, 3. 공정성 및 활동량 편향, 4. 실서버 지연, 5. 운영 관찰사항, 6. 최종 판정 (+1 more)

### Community 54 - "_Redis"
Cohesion: 0.17
Nodes (7): Exception, _Connection, _Engine, 헬스체크는 내부 오류를 노출하지 않고 장애 시 HTTP 503을 반환한다., _Redis, test_health_degraded_is_503_and_hides_exception(), test_health_ok()

### Community 55 - "test_schema.py"
Cohesion: 0.33
Nodes (3): 스키마 v3 baseline 정합 검증 (설계: docs/superpowers/specs/2026-07-05-v2_1-refactor-desig, 탈퇴 익명화(§15): 게시물·댓글·채팅 발신자는 SET NULL 가능해야 한다., test_anonymizable_fks_nullable()

### Community 63 - "SAFE 그루밍 평가 결과"
Cohesion: 0.40
Nodes (4): SAFE 그루밍 평가 결과, 기존 3a holdout, 신규 합성셋 결과, 진단

### Community 64 - "get_current_user"
Cohesion: 0.25
Nodes (10): list_notifications(), mark_read(), NotificationListOut, NotificationOut, AsyncSession, ReadIn, get_current_user(), AsyncSession (+2 more)

### Community 66 - "ws.py"
Cohesion: 0.27
Nodes (9): Redis, WS /api/v1/ws?token=<access> — 새 메시지·알림 실시간 푸시. 인증은 JWT 검증만으로 처리(DB 미조회)해 연결…, _relay(), ws_endpoint(), get_redis(), get_redis_client(), Redis, FastAPI 의존성. 테스트에서 override 가능하도록 분리. (+1 more)

### Community 83 - "test_config.py"
Cohesion: 0.22
Nodes (8): Settings, BaseSettings, 테스트 전용 DB만 허용한다. 명시값이 없으면 현재 DB명에 `_test`를 붙인다., _test_database_url(), v2.1 명세 고정값이 Settings에 반영되어 있는지 검증., docker compose env_file은 POSTGRES_PASSWORD/REDIS_PASSWORD도 컨테이너 프로세스에 노출한다. 이…, test_settings_ignores_compose_only_env_vars(), test_tests_always_use_test_database()

### Community 84 - "blocks.py"
Cohesion: 0.36
Nodes (8): create_block(), list_blocks(), AsyncSession, UUID, BLOCK-01 사용자 차단 — 게시물·프로필·요청·채팅·추천 상호 제거., remove_block(), BlockIn, BlockListOut

### Community 85 - "stt.py"
Cohesion: 0.32
Nodes (7): _get_client(), AsyncOpenAI, OpenAI Whisper STT 서비스 (F02_S05 음성 댓글 / 자막).  엔드포인트는 `stt.transcribe(...)` 를 호출한, 오디오 바이트 → 한국어 전사 텍스트. (실제 Whisper 호출, VIS-03 음성 입력), 영상/오디오 → 자막 세그먼트 [{start, end, text}] (CAPTION-01)., transcribe(), transcribe_segments()

### Community 87 - "test_notifications.py"
Cohesion: 0.48
Nodes (6): _notis(), §16 알림 — 생성 훅·목록·읽음. WS 푸시는 test_ws에서 검증., test_comment_and_like_notify_author_not_self(), test_flagged_and_restriction_notify_receiver(), test_friend_request_and_accept_notifications(), test_mark_read()

### Community 88 - "env.py"
Cohesion: 0.60
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

### Community 89 - "withdraw"
Cohesion: 0.67
Nodes (3): AsyncSession, withdraw(), PostsAction

### Community 122 - "Chat Read Status Implementation Plan"
Cohesion: 0.25
Nodes (7): Chat Read Status Implementation Plan, File Structure, Global Constraints, Plan Self-Review, Task 1: Write failing behavior tests, Task 2: Persist and calculate the cursor, Task 3: Expose, document, verify, and commit

### Community 123 - "Task 1 — Failing behavior tests"
Cohesion: 0.29
Nodes (6): Changes, Read event, Required red-test commands, Self-review, Task 1 — Failing behavior tests, Unread badge and receipt

### Community 124 - "Task 2 report — persistence and cursor helpers"
Cohesion: 0.29
Nodes (6): Changes, P1 follow-up — atomic cursor advancement, P1 follow-up verification, Self-review, Task 2 report — persistence and cursor helpers, Verification

### Community 127 - "Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?, Source Nodes

### Community 128 - "Q: 백엔드 핵심 소스코드 2개와 설명"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 백엔드 핵심 소스코드 2개와 설명, Source Nodes

## Knowledge Gaps
- **257 isolated node(s):** `thisabled-backend`, `Chat Read Status SDD Ledger`, `Task 1: Write failing behavior tests`, `Changes`, `Unread badge and receipt` (+252 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `v1/chat.py`, `get_current_user`, `BaseModel`, `ai_media.py`, `friends.py`, `v1/media.py`, `v1/comm.py`, `match.py`, `blocks.py`, `v1/auth.py`, `withdraw`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `register()` connect `register` to `test_media.py`, `friends.py`, `test_chat.py`, `test_ws.py`, `test_auth.py`, `test_notifications.py`, `test_friends.py`, `conftest.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `auth_header()` connect `register` to `test_media.py`, `friends.py`, `test_chat.py`, `test_ws.py`, `test_auth.py`, `test_notifications.py`, `test_friends.py`, `conftest.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `User` (e.g. with `callback()` and `refresh()`) actually correct?**
  _`User` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Base` (e.g. with `ChatMessage` and `ChatReadState`) actually correct?**
  _`Base` has 20 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thisabled-backend`, `Chat Read Status SDD Ledger`, `Task 1: Write failing behavior tests` to the rest of the system?**
  _257 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `v1/chat.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06511761331038439 - nodes in this community are weakly interconnected._