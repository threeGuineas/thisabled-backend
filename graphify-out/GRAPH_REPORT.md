# Graph Report - thisabled-backend  (2026-08-15)

## Corpus Check
- 116 files · ~56,989 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1132 nodes · 2562 edges · 127 communities (73 shown, 54 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 168 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `da69753b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- services/chat.py
- users.py
- User
- ai_media.py
- ai_result_cache 테이블(미디어 해시 캐싱)
- friends.py
- v1/chat.py
- register
- blocks.py
- notify
- quota.py
- match_model.py
- test_auth.py
- oauth.py
- safe_grooming_eval.py
- 채팅 읽음 상태 설계
- ThisAbled API 명세 요약 (v2.2)
- MATCH-02 추천 입력
- test_oauth_real.py
- recommendations.py
- ThisAbled — Backend
- ThisAbled 기능 명세서 v2.2
- safety_model.py
- services/comm.py
- Q: 친구 추천 부분도 로딩이 안되는 문제가 있다고 하는데 확인 부탁함
- v1/auth.py
- Global Constraints
- SAFE 그루밍 평가 설계
- 14. 발달장애인 모드 및 AI 소통 코치
- 7. 피드·게시물·댓글
- conftest.py
- 11. AI 안심 채팅
- 1. 서비스 개요
- v1/media.py
- 4. 사용자 정책
- 10. 1:1 채팅
- 12. 시각장애인 모드
- test_openapi.py
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
- test_health.py
- is_minor
- SAFE 그루밍 평가 결과
- config.py
- test_config.py
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
- test_friends.py
- ws.py
- datetime
- thisabled-backend
- _BorrowedSession
- security.py
- real_oauth
- _frontend_redirect
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
- AsyncSession
- Google OAuth Setup
- Kakao OAuth Setup
- OAuth Mock Provider (dev)
- OAuth Redirect URI Decision
- Definition of Done 체크리스트
- Redis TTL 호출 한도 카운터(vision·caption)
- users 테이블
- Exception
- fixture
- delete
- async_sessionmaker
- BackgroundTasks
- UploadFile
- Chat Read Status Implementation Plan
- Any
- Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?
- Q: 백엔드 핵심 소스코드 2개와 설명

## God Nodes (most connected - your core abstractions)
1. `register()` - 67 edges
2. `auth_header()` - 64 edges
3. `User` - 60 edges
4. `Base` - 29 edges
5. `_Redis` - 27 edges
6. `_post()` - 24 edges
7. `ChatMessage` - 23 edges
8. `ThisAbled 기능 명세서 v2.2` - 23 edges
9. `PostMedia` - 21 edges
10. `Post` - 20 edges

## Surprising Connections (you probably didn't know these)
- `test_exclusion_rules_enforced_by_backend()` --indirect_call--> `Block`  [INFERRED]
  tests/test_match.py → app/models/social.py
- `test_exclusion_rules_enforced_by_backend()` --indirect_call--> `FriendRequest`  [INFERRED]
  tests/test_match.py → app/models/social.py
- `test_normalize_pair_orders_by_uuid()` --calls--> `normalize_pair()`  [EXTRACTED]
  tests/test_age.py → app/core/pairs.py
- `test_cleanup_deletes_stale_drafts()` --indirect_call--> `Post`  [INFERRED]
  tests/test_media.py → app/models/post.py
- `test_withdraw_anonymize_keeps_posts_and_chat()` --indirect_call--> `Post`  [INFERRED]
  tests/test_withdrawal.py → app/models/post.py

## Import Cycles
- None detected.

## Communities (127 total, 54 thin omitted)

### Community 0 - "services/chat.py"
Cohesion: 0.08
Nodes (49): §CHAT-02 — request=요청함, active=일반 채팅., RoomState, ChatMessage, ChatReadState, ChatRoom, SAFE-05 관계 단위 자동 전송 제한. 누적 카운터는 별도 컬럼 없이 chat_messages에서 `flagged AND…, 1:1 채팅방 (CHAT-01/02). request=요청함, active=일반 채팅. 참여자는 정규화 쌍(user_a < user_b,…, 채팅 메시지 (SAFE-01~03). 텍스트는 동기 분석 후 저장·전달. (+41 more)

### Community 1 - "users.py"
Cohesion: 0.06
Nodes (60): do_run_migrations(), run_async_migrations(), run_migrations_online(), me(), _me_out(), patch_me(), patch_settings(), public_profile() (+52 more)

### Community 2 - "User"
Cohesion: 0.11
Nodes (56): _author_out(), _blocked_ids_subq(), caption_status(), _comment_out(), create_comment(), create_post(), delete_comment(), delete_post() (+48 more)

### Community 3 - "ai_media.py"
Cohesion: 0.13
Nodes (27): _cache_get(), _cache_put(), caption_chat_message_job(), caption_post_media_job(), consume_vision(), describe_chat_message_job(), describe_image(), describe_post_media_job() (+19 more)

### Community 5 - "friends.py"
Cohesion: 0.12
Nodes (39): accept_request(), _author(), cancel_request(), decline_request(), _get_pending(), list_friends(), list_requests(), AsyncSession (+31 more)

### Community 6 - "v1/chat.py"
Cohesion: 0.10
Nodes (45): accept_request(), _author(), create_room(), _get_my_room(), list_messages(), list_requests(), list_rooms(), _message_out() (+37 more)

### Community 7 - "register"
Cohesion: 0.05
Nodes (99): lifespan(), FastAPI, Block, 차단 (BLOCK-01). 게시물·프로필·요청·채팅·추천 접점을 상호 제거., user_channel(), get_safety_client(), Exception, SAFE-01 — 자체 안전 모델 HTTP 클라이언트 (별도 모델 서버 경계, AI 팀 담당). 텍스트 위험 판정에는 외부 AI를 사용하지… (+91 more)

### Community 8 - "blocks.py"
Cohesion: 0.20
Nodes (14): BlockedOut, create_block(), list_blocks(), AsyncSession, BaseModel, get, post, User (+6 more)

### Community 9 - "notify"
Cohesion: 0.16
Nodes (18): list_notifications(), mark_read(), NotificationListOut, NotificationOut, AsyncSession, BaseModel, get, post (+10 more)

### Community 10 - "quota.py"
Cohesion: 0.18
Nodes (17): caption_key(), _minute(), Redis TTL 카운터 — VISION-01·CAPTION-01 사용자별 호출 한도. 키는 날짜/분 단위로 자연 만료(TTL)되고, 자막…, 카운터 1 증가. 한도 초과면 롤백 후 False., CAPTION-01: 자막 생성 실패(재시도 소진) 시 일일 횟수 차감 복원., 이미지 1장 = 1회, 게시물·채팅 합산 (VISION-01). [(키, 한도, TTL), ...], 영상 업로드 = 1회 차감, 게시물·채팅 합산 (CAPTION-01)., refund() (+9 more)

### Community 11 - "match_model.py"
Cohesion: 0.32
Nodes (7): Features, health(), BaseModel, get, match-model mock — SBERT+LightGBM 모델 서버가 오기 전 자리 지킴이. 계약: POST /score {me,…, score(), ScoreIn

### Community 12 - "test_auth.py"
Cohesion: 0.29
Nodes (11): ACC-01/02 — 소셜 OAuth 전용 인증 (mock 제공자)., _signup_token(), test_callback_new_user_redirects_with_signup_token(), test_refresh_rotates_access_token(), test_rejoin_blocked_within_30_days(), test_signup_duplicate_nickname(), test_signup_forbidden_nickname(), test_signup_minor_blocks_stranger_requests() (+3 more)

### Community 13 - "oauth.py"
Cohesion: 0.09
Nodes (14): get_provider(), GoogleProvider, _http(), KakaoProvider, MockProvider, OAuthProvider, OAuthUserInfo, AsyncClient (+6 more)

### Community 14 - "safe_grooming_eval.py"
Cohesion: 0.24
Nodes (16): test_fixture_contains_detection_and_boundary_cases(), test_fixture_rows_match_case_schema(), test_invalid_case_is_rejected(), test_invalid_verdict_is_error_not_safe(), test_summarize_reports_recall_fnr_fpr_and_subgroups(), evaluate(), _group_metrics(), load_cases() (+8 more)

### Community 15 - "채팅 읽음 상태 설계"
Cohesion: 0.22
Nodes (8): API와 실시간 이벤트, 대안과 결정, 데이터 모델, 목표, 범위와 용어, 안전성과 일관성, 채팅 읽음 상태 설계, 테스트

### Community 16 - "ThisAbled API 명세 요약 (v2.2)"
Cohesion: 0.18
Nodes (10): auth (ACC-01/02), chat (CHAT-01~03 · SAFE-01~05), comm (COMM-01~05), friends / blocks (FRIEND-01/02 · BLOCK-01), media (VISION-01 · CAPTION-01 · VIS-03), notifications (§16) / ws, posts / feed (FEED-01 · POST-01~03), recommendations (MATCH) (+2 more)

### Community 17 - "MATCH-02 추천 입력"
Cohesion: 0.15
Nodes (13): 8. AI 사용자 매칭, MATCH-01 추천 목적, MATCH-02-1 자기소개, MATCH-02-2 관심사 태그, MATCH-02-3 사용자의 작성물, MATCH-02-4 분석 제외 데이터, MATCH-02-5 연령 정보, MATCH-02-6 좋아요 기반 관심 신호 (+5 more)

### Community 18 - "test_oauth_real.py"
Cohesion: 0.16
Nodes (15): callback_params(), 콜백 302 리다이렉트(Location=FRONTEND_URL?…)의 쿼리 파라미터 → 단일값 dict., test_existing_user_callback_logs_in(), test_invalid_mock_code_redirects_with_error(), _google_transport(), _kakao_transport(), 실 제공자(카카오·구글) OAuth 경로 — 외부 API를 MockTransport로 대체해 검증. 실키 없이 코드 경로(파라미터 인코딩·토큰…, 제공자가 거부한 code(만료·재사용)도 프론트로 error 리다이렉트. (+7 more)

### Community 19 - "recommendations.py"
Cohesion: 0.09
Nodes (24): AsyncSession, BaseModel, get, RecommendationListOut, RecommendationOut, recommendations(), candidate_pool(), get_match_client() (+16 more)

### Community 20 - "ThisAbled — Backend"
Cohesion: 0.15
Nodes (12): DB 스키마 (v3), graphify, Ralph 루프 (선택), ThisAbled — Backend, 기술 스택, 데드라인, 링크, 명령어 (+4 more)

### Community 21 - "ThisAbled 기능 명세서 v2.2"
Cohesion: 0.20
Nodes (9): 15. 마이페이지·설정, 16. 알림, 20. 핵심 인수 조건, 21. MVP 이후 계획, 2. 핵심 기능명, 3.1 포함, 3.2 제외 및 후속 범위, 3. MVP 범위 (+1 more)

### Community 22 - "safety_model.py"
Cohesion: 0.33
Nodes (6): analyze(), AnalyzeIn, health(), BaseModel, get, safety-model mock — AI 팀원의 자체 파인튜닝 안전 모델 서버가 오기 전 자리 지킴이. 계약: POST /analyze…

### Community 23 - "services/comm.py"
Cohesion: 0.07
Nodes (24): _collect_strings(), CommUnavailable, get_comm_client(), OpenAICommClient, _plain_text(), COMM — LLM 소통 코치 (외부 API, §17.2 고지 대상). 버튼 실행 시에만 동작(COMM-05). 채팅 컨텍스트는 최근 N개…, FastAPI 의존성 — 테스트에서 fake로 override., 외부 코칭 결과를 안전한 API 응답으로 만들 수 없을 때. (+16 more)

### Community 24 - "Q: 친구 추천 부분도 로딩이 안되는 문제가 있다고 하는데 확인 부탁함"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 친구 추천 부분도 로딩이 안되는 문제가 있다고 하는데 확인 부탁함, Source Nodes

### Community 25 - "v1/auth.py"
Cohesion: 0.19
Nodes (20): authorize(), callback(), logout(), AsyncSession, get, UUID, ACC-01/02 — 소셜 OAuth 전용 인증. 흐름: authorize → 제공자 로그인 → callback → FRONTEND_URL로…, refresh() (+12 more)

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
Cohesion: 0.20
Nodes (15): get_session_factory(), 백그라운드 작업(자막·설명 부착)용 세션 팩토리. 테스트에서 override., client(), _conn(), db(), _force_oauth_mock(), AsyncClient, fixture (+7 more)

### Community 31 - "11. AI 안심 채팅"
Cohesion: 0.33
Nodes (6): 11. AI 안심 채팅, SAFE-01 분석 원칙과 전달 타이밍, SAFE-02 탐지 범위, SAFE-03 사용자 표시, SAFE-04 내부 위험 점수, SAFE-05 관계 단위 자동 전송 제한 (신설)

### Community 32 - "1. 서비스 개요"
Cohesion: 0.33
Nodes (6): 1.1 서비스명, 1.2 서비스 정의 (한 문장), 1.3 서비스 비전, 1.4 해결하려는 문제, 1.5 핵심 사용자 경험, 1. 서비스 개요

### Community 33 - "v1/media.py"
Cohesion: 0.13
Nodes (24): async_sessionmaker, AsyncSession, BackgroundTasks, UploadFile, 미디어 업로드 — 사진(≤3장) · 영상(드래프트+자막 시작) · VIS-03 음성 입력., VIS-03 음성 입력 — 결과는 입력란 삽입용. 자동 게시하지 않는다 (§20-4)., 사진 업로드 (post 미연결) — POST /posts 의 media_ids로 연결한다., 영상 첨부 = processing 내부 드래프트 생성 + 자막 생성 즉시 시작 (POST-01·CAPTION-01). 길이(≤3분)는 FE가… (+16 more)

### Community 34 - "4. 사용자 정책"
Cohesion: 0.33
Nodes (6): 4.1 가입 대상, 4.2 장애인 자격 확인, 4.3 복합장애, 4.4 콘텐츠 공개, 4.5 미성년자 보호 (신설), 4. 사용자 정책

### Community 35 - "10. 1:1 채팅"
Cohesion: 0.40
Nodes (5): 10. 1:1 채팅, CHAT-01 친구 채팅, CHAT-02 비친구 메시지 요청, CHAT-03 채팅 상태, CHAT-04 읽음·안읽음 표시 (신설)

### Community 36 - "12. 시각장애인 모드"
Cohesion: 0.40
Nodes (5): 12. 시각장애인 모드, VIS-01 기본 UI, VIS-02 스크린리더, VIS-03 음성 입력, VIS-04 상태 안내

### Community 37 - "test_openapi.py"
Cohesion: 0.19
Nodes (14): Any, _add_error_response(), _guide(), install_openapi(), OperationGuide, FastAPI, 프론트엔드 구현자를 위한 OpenAPI 문서 보강. FastAPI의 기본 스키마는 타입은 정확하지만 비즈니스 상태와 화면 처리 방법을 설명하지…, 프론트엔드 계약 문서가 라우트 변경 뒤에도 빠지거나 퇴행하지 않도록 검증. (+6 more)

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
Cohesion: 0.18
Nodes (29): _coach(), complete(), hints(), HintsOut, _post_context(), PostIn, AsyncSession, BaseModel (+21 more)

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

### Community 54 - "test_health.py"
Cohesion: 0.13
Nodes (10): health(), HealthOut, BaseModel, get, _Connection, _Engine, Exception, 헬스체크는 내부 오류를 노출하지 않고 장애 시 HTTP 503을 반환한다. (+2 more)

### Community 55 - "is_minor"
Cohesion: 0.29
Nodes (12): age_band(), full_age(), is_minor(), 만 나이 계산 (§4.5 미성년 보호, MATCH-02-5 연령대). 생년월일 원문은 저장만 하고 파생값(만 나이·연령대·미성년)은 항상 요청…, 만 14~18세 미성년 보호 대상 여부 (§4.5). 만 13 이하는 가입 자체가 불가., MATCH-02-5 연령대. 추천 특성으로만 사용, 생년월일 원문은 모델에 전달하지 않는다., date, 만 나이·연령대·쌍 정규화 유틸 (§4.5, MATCH-02-5). (+4 more)

### Community 63 - "SAFE 그루밍 평가 결과"
Cohesion: 0.40
Nodes (4): SAFE 그루밍 평가 결과, 기존 3a holdout, 신규 합성셋 결과, 진단

### Community 64 - "config.py"
Cohesion: 0.13
Nodes (16): get_redis(), get_redis_client(), FastAPI 의존성. 테스트에서 override 가능하도록 분리., _get_client(), AsyncOpenAI, OpenAI Whisper STT 서비스 (F02_S05 음성 댓글 / 자막). 엔드포인트는 `stt.transcribe(...)` 를…, 오디오 바이트 → 한국어 전사 텍스트. (실제 Whisper 호출, VIS-03 음성 입력), 영상/오디오 → 자막 세그먼트 [{start, end, text}] (CAPTION-01). (+8 more)

### Community 66 - "test_config.py"
Cohesion: 0.22
Nodes (8): Settings, BaseSettings, 테스트 전용 DB만 허용한다. 명시값이 없으면 현재 DB명에 `_test`를 붙인다., _test_database_url(), v2.1 명세 고정값이 Settings에 반영되어 있는지 검증., docker compose env_file은 POSTGRES_PASSWORD/REDIS_PASSWORD도 컨테이너 프로세스에 노출한다. 이…, test_settings_ignores_compose_only_env_vars(), test_tests_always_use_test_database()

### Community 83 - "test_friends.py"
Cohesion: 0.44
Nodes (9): _pair(), FRIEND-01/02 친구 요청·관리 · BLOCK-01 차단., _request(), test_block_removes_friendship_and_hides_everything(), test_cancel_only_by_sender(), test_decline_records_and_duplicate_pending_rejected(), test_request_accept_creates_mutual_friendship(), test_self_request_rejected() (+1 more)

### Community 84 - "ws.py"
Cohesion: 0.36
Nodes (7): WS /api/v1/ws?token=<access> — 새 메시지·알림 실시간 푸시. 인증은 JWT 검증만으로 처리(DB 미조회)해 연결…, _relay(), ws_endpoint(), decode_signup_token(), decode_token(), → (provider, provider_user_id). 위조·만료 시 JWTError., WebSocket

### Community 85 - "datetime"
Cohesion: 0.20
Nodes (7): AiStatus, MediaType, v2.2 도메인 enum. DB에는 String으로 저장한다 (PG enum 마이그레이션 부담 회피)., description_status / caption_status 공용., MATCH — 후보 풀·제외 조건은 백엔드가 강제하고, 점수·사유만 모델 서버에 위임. 제외(MATCH-03·02-5): 자신 / 이미 친구…, APScheduler 인프로세스 크론 — 24h 드래프트 청소 (+ Task 11에서 미분석 재분석 추가)., datetime

### Community 88 - "security.py"
Cohesion: 0.46
Nodes (7): create_access_token(), create_refresh_token(), create_signup_token(), _encode(), JWT 토큰 (access/refresh/signup). 소셜 OAuth 전용이라 비밀번호 해시는 없다 (ACC-01)., 콜백에서 신규 사용자에게 발급 — 추가 정보 입력(signup) 완료까지의 단기 자격., timedelta

### Community 89 - "real_oauth"
Cohesion: 0.67
Nodes (3): fixture, OAUTH_MOCK 해제 + 테스트용 가짜 키 주입., real_oauth()

### Community 90 - "_frontend_redirect"
Cohesion: 0.67
Nodes (3): _frontend_redirect(), 콜백 결과를 프론트 SPA로 302 전달 — 브라우저가 직접 호출하므로 JSON 대신 리다이렉트., RedirectResponse

### Community 122 - "Chat Read Status Implementation Plan"
Cohesion: 0.25
Nodes (7): Chat Read Status Implementation Plan, File Structure, Global Constraints, Plan Self-Review, Task 1: Write failing behavior tests, Task 2: Persist and calculate the cursor, Task 3: Expose, document, verify, and commit

### Community 127 - "Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?, Source Nodes

### Community 128 - "Q: 백엔드 핵심 소스코드 2개와 설명"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 백엔드 핵심 소스코드 2개와 설명, Source Nodes

## Knowledge Gaps
- **184 isolated node(s):** `thisabled-backend`, `프로젝트`, `기술 스택`, `명령어`, `DB 스키마 (v3)` (+179 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **54 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `recommendations()` (2× useful, score=1.999747624)
- `UiMode` (2× useful, score=1.999747624)
- `user_features()` (2× useful, score=1.999747624)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `services/chat.py`, `v1/media.py`, `users.py`, `friends.py`, `v1/comm.py`, `recommendations.py`, `v1/auth.py`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `auth_header()` connect `register` to `services/chat.py`, `test_auth.py`, `test_oauth_real.py`, `test_friends.py`, `conftest.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `register()` connect `register` to `services/chat.py`, `test_auth.py`, `test_oauth_real.py`, `test_friends.py`, `conftest.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `User` (e.g. with `callback()` and `refresh()`) actually correct?**
  _`User` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Base` (e.g. with `ChatMessage` and `ChatReadState`) actually correct?**
  _`Base` has 20 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thisabled-backend`, `프로젝트`, `기술 스택` to the rest of the system?**
  _184 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `services/chat.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0841799709724238 - nodes in this community are weakly interconnected._