# Graph Report - thisabled-backend  (2026-08-28)

## Corpus Check
- 146 files · ~70,254 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1447 nodes · 3331 edges · 151 communities (101 shown, 50 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 291 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `59ba4337`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- validate_nickname
- blocks.py
- posts.py
- v1/chat.py
- ai_result_cache 테이블(미디어 해시 캐싱)
- _Redis
- match_model.py
- v1/comm.py
- match.py
- caption_chat_message_job
- quota.py
- Q: 다 구현해줘 & 전체적으로 리팩토링도 필요할거같아 더 깔끔하고 체계적이고 직관적이게 & 또한 전체적으로 결함 탐색+보강이 필요해보이넹 & 지금까지 한것들 커밋들 브랜치 따로 영역에 맞게 분류해서 작업해줘
- StrictRequest
- oauth.py
- safe_grooming_eval.py
- 채팅 읽음 상태 설계
- ThisAbled API 명세 요약 (v2.3)
- services/chat.py
- User
- test_chat.py
- ThisAbled — Backend
- safety_model.py
- test_auth.py
- services/comm.py
- Q: 친구 추천 부분도 로딩이 안되는 문제가 있다고 하는데 확인 부탁함
- Q: 피그마 기준으로 게시물 카테고리 포함해서 누락된 백엔드 영역 기능 사항들 점검해줘
- Global Constraints
- SAFE 그루밍 평가 설계
- MATCH-02 추천 입력
- pull_request_template.md
- v1/auth.py
- ThisAbled 기능 명세서 v2.3
- test_safe.py
- test_notifications.py
- upload_video
- test_config.py
- test_ws.py
- test_openapi.py
- SAFE 이진 v6 배포 검증
- 14. 발달장애인 모드 및 AI 소통 코치
- 7. 피드·게시물·댓글
- 10. 1:1 채팅
- ai_media.py
- SAFE 최신 호환 서빙 재평가
- 11. AI 안심 채팅
- 1. 서비스 개요
- 4. 사용자 정책
- is_minor
- storage.py
- MATCH v2 배포 성능 평가
- friendships 테이블(정규화 쌍)
- WebSocket + Redis pub/sub 팬아웃
- withdrawn_socials 테이블
- config.py
- Q: 영상 첨부해서 게시하기 버튼 누르고 난 뒤 생기는 오류 Field required (오류 코드: 422) 이거 머임?
- SAFE 그루밍 평가 결과
- Q: post 필드에 원래 title 필드가 요구되지 않았던거같은데 왜이렇게 된거지?
- Q: 영상 자막 부분 계속 오류난다는데 다시 확인해봐
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
- Q: ㅇㅇ 수정 ㄱㄱ 그리고 [api 문서](https://ideal-macmini.tail72b898.ts.net/docs) 자세하게, 결함 없게 구체적으로 아주 친절하게 패치해줘 프론트엔드가 곤란하지 않도록
- Q: 영상 자막 부분 기능 감사해줘
- thisabled-backend
- Q: ㅇㅋ 결함들 해결 방안 추천해줘
- Q: 영상 자막 결함 해결 방안 구현
- 0. 문서 정보
- 12. 시각장애인 모드
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
- conftest.py
- Google OAuth Setup
- Kakao OAuth Setup
- OAuth Mock Provider (dev)
- OAuth Redirect URI Decision
- Definition of Done 체크리스트
- Redis TTL 호출 한도 카운터(vision·caption)
- users 테이블
- register
- 17. 외부 AI 사용 및 데이터 처리 원칙
- 6. 회원가입 및 계정
- Q: 자막 생성 때문에
- worker.py
- Chat Read Status Implementation Plan
- vision.py
- Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?
- Q: 백엔드 핵심 소스코드 2개와 설명
- notify.py
- test_match.py
- CHAT-05 음성·영상 통화 시그널링 설계
- 13. 청각장애인 모드
- test_friends.py
- 18. 기술 구성
- 19. 비기능 요구사항
- CaptionTranscriptionError
- 5. 공통 화면 구조
- 9. 친구·차단
- security.py
- redis.py
- media_probe.py
- Q: 아니 생각해보니까 이전 버전 기능명세도 2.2 버전인데 왜 수정했는데 v2.2로 그대로 가는거임? v2.3으로 업데이트 안함?
- Q: Run uv run pytest -q
- CallCounter
- datetime
- delete
- patch
- RuntimeError
- StrEnum

## God Nodes (most connected - your core abstractions)
1. `register()` - 91 edges
2. `auth_header()` - 88 edges
3. `StrictRequest` - 73 edges
4. `User` - 45 edges
5. `_Redis` - 39 edges
6. `Base` - 29 edges
7. `_room()` - 27 edges
8. `ChatMessage` - 25 edges
9. `make_friends()` - 25 edges
10. `_post()` - 25 edges

## Surprising Connections (you probably didn't know these)
- `match()` --indirect_call--> `get_match_client()`  [INFERRED]
  tests/test_match.py → app/services/match.py
- `FakeSafety` --uses--> `SafetyUnavailable`  [INFERRED]
  tests/test_chat.py → app/services/safety.py
- `test_normalize_pair_orders_by_uuid()` --calls--> `normalize_pair()`  [EXTRACTED]
  tests/test_age.py → app/core/pairs.py
- `test_cleanup_deletes_stale_drafts()` --indirect_call--> `Post`  [INFERRED]
  tests/test_media.py → app/models/post.py
- `test_photo_post_gets_description_on_publish()` --indirect_call--> `PostMedia`  [INFERRED]
  tests/test_media.py → app/models/post.py

## Import Cycles
- None detected.

## Communities (151 total, 50 thin omitted)

### Community 0 - "validate_nickname"
Cohesion: 0.40
Nodes (4): AsyncSession, 닉네임 정책 (ACC-01): 2~12자 한글·영문·숫자, 금칙어·중복 불가., 형식(400) → 금칙어(400) → 중복(409) 순 검증. 통과 시 None., validate_nickname()

### Community 1 - "blocks.py"
Cohesion: 0.18
Nodes (18): BlockedOut, create_block(), list_blocks(), AsyncSession, BaseModel, delete, get, UUID (+10 more)

### Community 2 - "posts.py"
Cohesion: 0.09
Nodes (63): _author_out(), _blocked_ids_subq(), caption_status(), _comment_out(), _contains_pattern(), create_comment(), create_post(), _cursor_position() (+55 more)

### Community 3 - "v1/chat.py"
Cohesion: 0.13
Nodes (47): accept_request(), _author(), create_room(), get_call(), _get_my_room(), _latest_messages(), list_messages(), list_requests() (+39 more)

### Community 5 - "_Redis"
Cohesion: 0.17
Nodes (7): _Connection, _Engine, Exception, 헬스체크는 내부 오류를 노출하지 않고 장애 시 HTTP 503을 반환한다., _Redis, test_health_degraded_is_503_and_hides_exception(), test_health_ok()

### Community 6 - "match_model.py"
Cohesion: 0.32
Nodes (7): Features, health(), BaseModel, get, match-model mock — SBERT+LightGBM 모델 서버가 오기 전 자리 지킴이. 계약: POST /score {me,…, score(), ScoreIn

### Community 7 - "v1/comm.py"
Cohesion: 0.07
Nodes (72): _coach(), complete(), hints(), HintsOut, _post_context(), PostIn, AsyncSession, BaseModel (+64 more)

### Community 8 - "match.py"
Cohesion: 0.12
Nodes (24): AsyncSession, BaseModel, get, RecommendationListOut, RecommendationOut, recommendations(), CloudIdentityError, _fetch() (+16 more)

### Community 9 - "caption_chat_message_job"
Cohesion: 0.15
Nodes (21): content_type_from_path(), STT multipart에 파일 확장자와 일치하는 실제 MIME을 제공한다., get_redis_client(), 현재 이벤트 루프 전용 클라이언트. asyncio Redis 연결을 다른 루프에서 재사용하면 Future/transport가 깨지므로…, _acquire_caption_lock(), caption_chat_message_job(), caption_post_media_job(), describe_chat_message_job() (+13 more)

### Community 10 - "quota.py"
Cohesion: 0.12
Nodes (31): _refund_unattempted_caption(), caption_global_key(), caption_key(), caption_refund_marker(), consume_caption(), consume_caption_retry_attempt(), _minute(), Redis TTL 카운터 — VISION-01·CAPTION-01 사용자·서비스 전체 호출 한도. 키는 날짜/분 단위로 자연… (+23 more)

### Community 11 - "Q: 다 구현해줘 & 전체적으로 리팩토링도 필요할거같아 더 깔끔하고 체계적이고 직관적이게 & 또한 전체적으로 결함 탐색+보강이 필요해보이넹 & 지금까지 한것들 커밋들 브랜치 따로 영역에 맞게 분류해서 작업해줘"
Cohesion: 0.50
Nodes (3): Answer, Outcome, Q: 다 구현해줘 & 전체적으로 리팩토링도 필요할거같아 더 깔끔하고 체계적이고 직관적이게 & 또한 전체적으로 결함 탐색+보강이 필요해보이넹 & 지금까지 한것들 커밋들 브랜치 따로 영역에 맞게 분류해서 작업해줘

### Community 12 - "StrictRequest"
Cohesion: 0.06
Nodes (81): me(), _me_out(), patch_me(), patch_settings(), public_profile(), put_mode(), put_tags(), AsyncSession (+73 more)

### Community 13 - "oauth.py"
Cohesion: 0.08
Nodes (17): get_provider(), GoogleProvider, _http(), KakaoProvider, MockProvider, OAuthProvider, OAuthUserInfo, AsyncClient (+9 more)

### Community 14 - "safe_grooming_eval.py"
Cohesion: 0.24
Nodes (16): test_fixture_contains_detection_and_boundary_cases(), test_fixture_rows_match_case_schema(), test_invalid_case_is_rejected(), test_invalid_verdict_is_error_not_safe(), test_summarize_reports_recall_fnr_fpr_and_subgroups(), evaluate(), _group_metrics(), load_cases() (+8 more)

### Community 15 - "채팅 읽음 상태 설계"
Cohesion: 0.22
Nodes (8): API와 실시간 이벤트, 대안과 결정, 데이터 모델, 목표, 범위와 용어, 안전성과 일관성, 채팅 읽음 상태 설계, 테스트

### Community 16 - "ThisAbled API 명세 요약 (v2.3)"
Cohesion: 0.18
Nodes (10): auth (ACC-01/02), chat (CHAT-01~05 · SAFE-01~05), comm (COMM-01~05), friends / blocks (FRIEND-01/02 · BLOCK-01), media (VISION-01 · CAPTION-01 · VIS-03), notifications (§16) / ws, posts / feed (FEED-01 · POST-01~03), recommendations (MATCH) (+2 more)

### Community 17 - "services/chat.py"
Cohesion: 0.05
Nodes (71): do_run_migrations(), run_async_migrations(), run_migrations_online(), Base, ChatMessage, ChatReadState, ChatRoom, datetime (+63 more)

### Community 18 - "User"
Cohesion: 0.16
Nodes (31): accept_request(), _author(), cancel_request(), decline_request(), _get_pending(), list_friends(), list_requests(), AsyncSession (+23 more)

### Community 19 - "test_chat.py"
Cohesion: 0.19
Nodes (25): _describe_fake(), make_friends(), CHAT-01 친구 채팅 · CHAT-02 비친구 요청 · 미디어 제한 (§4.5)., _room(), _send(), test_chat_caption_failure_exposes_stable_code_without_recall(), test_chat_text_is_trimmed_and_limited(), test_chat_video_gets_caption_and_notifies_both_users() (+17 more)

### Community 20 - "ThisAbled — Backend"
Cohesion: 0.14
Nodes (13): API·기능명세 변경 승인 게이트, DB 스키마 (v3), graphify, Ralph 루프 (선택), ThisAbled — Backend, 기술 스택, 데드라인, 링크 (+5 more)

### Community 21 - "safety_model.py"
Cohesion: 0.33
Nodes (6): analyze(), AnalyzeIn, health(), BaseModel, get, safety-model mock — AI 팀원의 자체 파인튜닝 안전 모델 서버가 오기 전 자리 지킴이. 계약: POST /analyze…

### Community 22 - "test_auth.py"
Cohesion: 0.10
Nodes (33): §15: 탈퇴 후 30일 재가입 제한 판정용. users 행은 hard delete하고 여기에만 흔적., WithdrawnSocial, callback_params(), 콜백 302 리다이렉트(Location=FRONTEND_URL?…)의 쿼리 파라미터 → 단일값 dict., ACC-01/02 — 소셜 OAuth 전용 인증 (mock 제공자)., _signup_token(), test_callback_new_user_redirects_with_signup_token(), test_existing_user_callback_logs_in() (+25 more)

### Community 23 - "services/comm.py"
Cohesion: 0.07
Nodes (25): _collect_strings(), CommUnavailable, get_comm_client(), OpenAICommClient, _plain_text(), RuntimeError, COMM — LLM 소통 코치 (외부 API, §17.2 고지 대상). 버튼 실행 시에만 동작(COMM-05). 채팅 컨텍스트는 최근 N개…, FastAPI 의존성 — 테스트에서 fake로 override. (+17 more)

### Community 24 - "Q: 친구 추천 부분도 로딩이 안되는 문제가 있다고 하는데 확인 부탁함"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 친구 추천 부분도 로딩이 안되는 문제가 있다고 하는데 확인 부탁함, Source Nodes

### Community 25 - "Q: 피그마 기준으로 게시물 카테고리 포함해서 누락된 백엔드 영역 기능 사항들 점검해줘"
Cohesion: 0.50
Nodes (3): Answer, Outcome, Q: 피그마 기준으로 게시물 카테고리 포함해서 누락된 백엔드 영역 기능 사항들 점검해줘

### Community 26 - "Global Constraints"
Cohesion: 0.29
Nodes (6): Global Constraints, SAFE Grooming Evaluation Implementation Plan, Task 1: Add the evaluation fixture and pure metric tests, Task 2: Implement the pure evaluator and CLI, Task 3: Run the real SAFE evaluation, Task 4: Verify and document limitations

### Community 27 - "SAFE 그루밍 평가 설계"
Cohesion: 0.29
Nodes (6): SAFE 그루밍 평가 설계, 목적, 범위, 비범위, 성공 기준, 실행 흐름

### Community 28 - "MATCH-02 추천 입력"
Cohesion: 0.15
Nodes (13): 8. AI 사용자 매칭, MATCH-01 추천 목적, MATCH-02-1 자기소개, MATCH-02-2 관심사 태그, MATCH-02-3 사용자의 작성물, MATCH-02-4 분석 제외 데이터, MATCH-02-5 연령 정보, MATCH-02-6 좋아요 기반 관심 신호 (+5 more)

### Community 29 - "pull_request_template.md"
Cohesion: 0.50
Nodes (3): API·기능명세 변경 검수, 검증, 변경 사항

### Community 30 - "v1/auth.py"
Cohesion: 0.18
Nodes (20): authorize(), callback(), _frontend_redirect(), logout(), _oauth_state_key(), AsyncSession, get, UUID (+12 more)

### Community 31 - "ThisAbled 기능 명세서 v2.3"
Cohesion: 0.20
Nodes (9): 15. 마이페이지·설정, 16. 알림, 20. 핵심 인수 조건, 21. MVP 이후 계획, 2. 핵심 기능명, 3.1 포함, 3.2 제외 및 후속 범위, 3. MVP 범위 (+1 more)

### Community 32 - "test_safe.py"
Cohesion: 0.13
Nodes (20): get_safety_client(), FastAPI 의존성 — 테스트에서 fake로 override., FakeSafety, fixture, 돈' 포함 → flagged. fail=True → SafetyUnavailable (§18.3)., safety(), _friend_room(), fixture (+12 more)

### Community 33 - "test_notifications.py"
Cohesion: 0.43
Nodes (7): _notis(), §16 알림 — 생성 훅·목록·읽음. WS 푸시는 test_ws에서 검증., test_comment_and_like_notify_author_not_self(), test_disabled_notification_group_is_not_stored(), test_flagged_and_restriction_notify_receiver(), test_friend_request_and_accept_notifications(), test_mark_read()

### Community 34 - "upload_video"
Cohesion: 0.22
Nodes (13): async_sessionmaker, AsyncSession, BackgroundTasks, post, Redis, UploadFile, User, VIS-03 음성 입력 — 결과는 입력란 삽입용. 자동 게시하지 않는다 (§20-4). (+5 more)

### Community 35 - "test_config.py"
Cohesion: 0.20
Nodes (7): Settings, BaseSettings, v2.1 명세 고정값이 Settings에 반영되어 있는지 검증., docker compose env_file은 POSTGRES_PASSWORD/REDIS_PASSWORD도 컨테이너 프로세스에 노출한다. 이…, CI처럼 Docker 볼륨이 없는 환경에서도 테스트 수집 전 app import가 성공해야 한다., test_app_import_does_not_require_existing_upload_directory(), test_settings_ignores_compose_only_env_vars()

### Community 36 - "test_ws.py"
Cohesion: 0.16
Nodes (24): WS /api/v1/ws?token=<access> — 새 메시지·알림·통화 시그널 실시간 푸시. 인증은 JWT 검증만으로 처리(DB…, _relay(), ws_endpoint(), user_channel(), heartbeat(), mark_offline(), mark_online(), online_statuses() (+16 more)

### Community 37 - "test_openapi.py"
Cohesion: 0.16
Nodes (19): _add_error_response(), _guide(), install_openapi(), OperationGuide, Any, FastAPI, 프론트엔드 구현자를 위한 OpenAPI 문서 보강. FastAPI의 기본 스키마는 타입은 정확하지만 비즈니스 상태와 화면 처리 방법을 설명하지…, 프론트엔드 계약 문서가 라우트 변경 뒤에도 빠지거나 퇴행하지 않도록 검증. (+11 more)

### Community 38 - "SAFE 이진 v6 배포 검증"
Cohesion: 0.33
Nodes (5): FN, FP, SAFE 이진 v6 배포 검증, 백엔드 회귀 확인, 판정

### Community 39 - "14. 발달장애인 모드 및 AI 소통 코치"
Cohesion: 0.29
Nodes (7): 14. 발달장애인 모드 및 AI 소통 코치, COMM-01 쉬운 문장 변환, COMM-02 문장 완성, COMM-03 댓글·답장 추천, COMM-04 대화 힌트, COMM-05 데이터 처리 원칙, DEV-01 기본 UI

### Community 40 - "7. 피드·게시물·댓글"
Cohesion: 0.29
Nodes (7): 7. 피드·게시물·댓글, CAPTION-01 영상 자동 자막, FEED-01 홈 피드, POST-01 게시물 작성, POST-02 수정·삭제, POST-03 좋아요·댓글, VISION-01 AI 사진 설명

### Community 41 - "10. 1:1 채팅"
Cohesion: 0.33
Nodes (6): 10. 1:1 채팅, CHAT-01 친구 채팅, CHAT-02 비친구 메시지 요청, CHAT-03 채팅 상태, CHAT-04 읽음·안읽음 표시 (신설), CHAT-05 음성·영상 통화

### Community 42 - "ai_media.py"
Cohesion: 0.17
Nodes (17): _cache_get(), _cache_put(), CaptionGenerationResult, consume_vision(), describe_image(), generate_caption(), get_describe_caller(), get_text_transcriber() (+9 more)

### Community 43 - "SAFE 최신 호환 서빙 재평가"
Cohesion: 0.40
Nodes (4): SAFE 최신 호환 서빙 재평가, 결과, 결론, 실행 기준

### Community 44 - "11. AI 안심 채팅"
Cohesion: 0.33
Nodes (6): 11. AI 안심 채팅, SAFE-01 분석 원칙과 전달 타이밍, SAFE-02 탐지 범위, SAFE-03 사용자 표시, SAFE-04 내부 위험 점수, SAFE-05 관계 단위 자동 전송 제한 (신설)

### Community 45 - "1. 서비스 개요"
Cohesion: 0.33
Nodes (6): 1.1 서비스명, 1.2 서비스 정의 (한 문장), 1.3 서비스 비전, 1.4 해결하려는 문제, 1.5 핵심 사용자 경험, 1. 서비스 개요

### Community 46 - "4. 사용자 정책"
Cohesion: 0.33
Nodes (6): 4.1 가입 대상, 4.2 장애인 자격 확인, 4.3 복합장애, 4.4 콘텐츠 공개, 4.5 미성년자 보호 (신설), 4. 사용자 정책

### Community 47 - "is_minor"
Cohesion: 0.29
Nodes (12): age_band(), full_age(), is_minor(), 만 나이 계산 (§4.5 미성년 보호, MATCH-02-5 연령대). 생년월일 원문은 저장만 하고 파생값(만 나이·연령대·미성년)은 항상 요청…, 만 14~18세 미성년 보호 대상 여부 (§4.5). 만 13 이하는 가입 자체가 불가., MATCH-02-5 연령대. 추천 특성으로만 사용, 생년월일 원문은 모델에 전달하지 않는다., date, 만 나이·연령대·쌍 정규화 유틸 (§4.5, MATCH-02-5). (+4 more)

### Community 48 - "storage.py"
Cohesion: 0.20
Nodes (13): delete_upload(), _ext_from_content_type(), Exception, Path, Protocol, Save file locally and return the public URL path., 업로드를 메모리에 통째로 올리지 않고 저장하며 크기와 SHA-256을 계산한다., save_upload() (+5 more)

### Community 50 - "MATCH v2 배포 성능 평가"
Cohesion: 0.20
Nodes (9): 1. 기동 및 계약, 2.1 배포 번들 저장 지표, 2.2 배포 모델 독립 재평가, 2. 랭킹 품질, 3. 공정성 및 활동량 편향, 4. 실서버 지연, 5. 운영 관찰사항, 6. 최종 판정 (+1 more)

### Community 54 - "config.py"
Cohesion: 0.11
Nodes (23): health(), HealthOut, BaseModel, get, 미디어 업로드 — 사진(≤3장) · 영상(드래프트+자막 시작) · VIS-03 음성 입력., list_notifications(), mark_read(), NotificationListOut (+15 more)

### Community 55 - "Q: 영상 첨부해서 게시하기 버튼 누르고 난 뒤 생기는 오류 Field required (오류 코드: 422) 이거 머임?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 영상 첨부해서 게시하기 버튼 누르고 난 뒤 생기는 오류 Field required (오류 코드: 422) 이거 머임?, Source Nodes

### Community 63 - "SAFE 그루밍 평가 결과"
Cohesion: 0.40
Nodes (4): SAFE 그루밍 평가 결과, 기존 3a holdout, 신규 합성셋 결과, 진단

### Community 64 - "Q: post 필드에 원래 title 필드가 요구되지 않았던거같은데 왜이렇게 된거지?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: post 필드에 원래 title 필드가 요구되지 않았던거같은데 왜이렇게 된거지?, Source Nodes

### Community 66 - "Q: 영상 자막 부분 계속 오류난다는데 다시 확인해봐"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 영상 자막 부분 계속 오류난다는데 다시 확인해봐, Source Nodes

### Community 84 - "Q: ㅇㅇ 수정 ㄱㄱ 그리고 [api 문서](https://ideal-macmini.tail72b898.ts.net/docs) 자세하게, 결함 없게 구체적으로 아주 친절하게 패치해줘 프론트엔드가 곤란하지 않도록"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ㅇㅇ 수정 ㄱㄱ 그리고 [api 문서](https://ideal-macmini.tail72b898.ts.net/docs) 자세하게, 결함 없게 구체적으로 아주 친절하게 패치해줘 프론트엔드가 곤란하지 않도록, Source Nodes

### Community 85 - "Q: 영상 자막 부분 기능 감사해줘"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 영상 자막 부분 기능 감사해줘, Source Nodes

### Community 87 - "Q: ㅇㅋ 결함들 해결 방안 추천해줘"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ㅇㅋ 결함들 해결 방안 추천해줘, Source Nodes

### Community 88 - "Q: 영상 자막 결함 해결 방안 구현"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 영상 자막 결함 해결 방안 구현, Source Nodes

### Community 89 - "0. 문서 정보"
Cohesion: 0.40
Nodes (5): 0.0 v2.3 주요 개정 사항, 0.1 v2.2 주요 개정 사항 (이력), 0.2 v2.1 주요 개정 사항 (이력), 0.3 v2.0 주요 개정 사항 (이력), 0. 문서 정보

### Community 90 - "12. 시각장애인 모드"
Cohesion: 0.40
Nodes (5): 12. 시각장애인 모드, VIS-01 기본 UI, VIS-02 스크린리더, VIS-03 음성 입력, VIS-04 상태 안내

### Community 108 - "conftest.py"
Cohesion: 0.13
Nodes (19): get_session_factory(), 백그라운드 작업(자막·설명 부착)용 세션 팩토리. 테스트에서 override., _BorrowedSession, client(), _conn(), _force_oauth_mock(), _isolate_upload_directory(), AsyncClient (+11 more)

### Community 116 - "register"
Cohesion: 0.11
Nodes (48): 모드 변경 이력 (§5.2, 베타테스트 분석용)., UserModeHistory, cleanup_stale_drafts(), CAPTION-01: 업로드 후 24시간 미게시 내부 드래프트를 영상·자막과 함께 삭제. 이미 성공한 자막 생성의 일일 횟수 차감은 복원하지…, auth_header(), mock OAuth 가입 헬퍼 → {access_token, user_id, ...}., register(), VISION-01 사진 설명 · CAPTION-01 영상 자막 · VIS-03 음성 입력 · 24h 드래프트 청소. (+40 more)

### Community 117 - "17. 외부 AI 사용 및 데이터 처리 원칙"
Cohesion: 0.40
Nodes (5): 17.1 자체 처리 (외부 미전송), 17.2 외부 AI API 사용 (가입 시 필수 고지), 17.3 공통 처리 원칙, 17.4 관리자 기능, 17. 외부 AI 사용 및 데이터 처리 원칙

### Community 118 - "6. 회원가입 및 계정"
Cohesion: 0.40
Nodes (5): 6. 회원가입 및 계정, ACC-01 회원가입 (소셜 로그인), ACC-02 로그인·로그아웃, ACC-03 프로필, TAG-01 관심사 태그 체계 (정본)

### Community 120 - "Q: 자막 생성 때문에"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 자막 생성 때문에, Source Nodes

### Community 121 - "worker.py"
Cohesion: 0.12
Nodes (20): AiTaskKind, _create_cloud_task(), AI 미디어 작업을 로컬 BackgroundTasks 또는 Cloud Tasks로 전달한다., AiTaskIn, health(), lifespan(), BaseModel, FastAPI (+12 more)

### Community 122 - "Chat Read Status Implementation Plan"
Cohesion: 0.25
Nodes (7): Chat Read Status Implementation Plan, File Structure, Global Constraints, Plan Self-Review, Task 1: Write failing behavior tests, Task 2: Persist and calculate the cursor, Task 3: Expose, document, verify, and commit

### Community 126 - "vision.py"
Cohesion: 0.40
Nodes (5): generate_description(), _get_client(), AsyncOpenAI, GPT-4o Vision 이미지 해설 서비스 (F02_S04 시각장애 모드). 엔드포인트는…, 이미지 바이트 → 한국어 해설 텍스트. (실제 GPT-4o 호출)

### Community 127 - "Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?, Source Nodes

### Community 128 - "Q: 백엔드 핵심 소스코드 2개와 설명"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 백엔드 핵심 소스코드 2개와 설명, Source Nodes

### Community 129 - "notify.py"
Cohesion: 0.29
Nodes (8): _notify_chat_caption(), _notify_post_caption(), publish_to_user(), 실시간 이벤트 — Redis pub/sub 팬아웃 (다중 워커에서도 사용자별 채널로 전달). event 형식: {"type":…, _enabled(), notify(), AsyncSession, §16 알림 생성 — DB 저장 + WS 푸시 병행. 표현(시각·음성·진동)은 FE가 모드별 처리.

### Community 130 - "test_match.py"
Cohesion: 0.18
Nodes (9): FakeMatch, match(), fixture, MATCH — 후보 제외 규칙은 백엔드 강제, 점수·사유는 모델 서버 (mock/fake)., 도메인 default는 MATCH 서버가 허용하는 중립값으로 직렬화한다., test_default_mode_uses_neutral_model_value(), test_empty_pool_message(), test_exclusion_rules_enforced_by_backend() (+1 more)

### Community 131 - "CHAT-05 음성·영상 통화 시그널링 설계"
Cohesion: 0.29
Nodes (6): API와 이벤트, CHAT-05 음성·영상 통화 시그널링 설계, 검증, 목표와 경계, 오류 계약, 정책

### Community 132 - "13. 청각장애인 모드"
Cohesion: 0.50
Nodes (4): 13. 청각장애인 모드, HEAR-01 기본 UI, HEAR-02 영상 자막, HEAR-03 알림

### Community 133 - "test_friends.py"
Cohesion: 0.44
Nodes (9): _pair(), FRIEND-01/02 친구 요청·관리 · BLOCK-01 차단., _request(), test_block_removes_friendship_and_hides_everything(), test_cancel_only_by_sender(), test_decline_records_and_duplicate_pending_rejected(), test_request_accept_creates_mutual_friendship(), test_self_request_rejected() (+1 more)

### Community 134 - "18. 기술 구성"
Cohesion: 0.50
Nodes (4): 18.1 웹 서비스, 18.2 AI 모듈, 18.3 설계 원칙, 18. 기술 구성

### Community 135 - "19. 비기능 요구사항"
Cohesion: 0.50
Nodes (4): 19.1 접근성, 19.2 개인정보·보안, 19.3 AI 품질, 19. 비기능 요구사항

### Community 136 - "CaptionTranscriptionError"
Cohesion: 0.12
Nodes (23): caption_failure_details(), caption_failure_state(), CaptionFailureDetails, CaptionTranscriptionError, RuntimeError, CAPTION-01 실패 코드와 프론트 표시용 안전한 메시지., 호출자가 자동 재시도 여부를 판단할 수 있는 자막 처리 오류., failed 상태에만 안정적인 코드·표시 문구·재시도 가능 여부를 노출한다. (+15 more)

### Community 137 - "5. 공통 화면 구조"
Cohesion: 0.50
Nodes (4): 5.1 주요 화면, 5.2 UI 모드 전환, 5.3 기본 모드 (GEN-01, 신설), 5. 공통 화면 구조

### Community 138 - "9. 친구·차단"
Cohesion: 0.50
Nodes (4): 9. 친구·차단, BLOCK-01 사용자 차단, FRIEND-01 친구 요청, FRIEND-02 친구 관리

### Community 139 - "security.py"
Cohesion: 0.46
Nodes (7): create_access_token(), create_refresh_token(), create_signup_token(), _encode(), JWT 토큰 (access/refresh/signup). 소셜 OAuth 전용이라 비밀번호 해시는 없다 (ACC-01)., 콜백에서 신규 사용자에게 발급 — 추가 정보 입력(signup) 완료까지의 단기 자격., timedelta

### Community 141 - "redis.py"
Cohesion: 0.29
Nodes (6): close_redis_client(), get_redis(), FastAPI 의존성. 테스트에서 override 가능하도록 분리., 현재 워커 이벤트 루프의 연결 풀을 애플리케이션 종료 시 정리한다., 이벤트 루프별 Redis 클라이언트 생성·종료 수명주기., test_current_loop_redis_client_is_reused_and_closed()

### Community 142 - "media_probe.py"
Cohesion: 0.38
Nodes (6): get_video_probe(), InvalidVideo, probe_video_duration(), Exception, Path, 서버가 직접 영상 컨테이너와 재생 시간을 검증한다.

### Community 143 - "Q: 아니 생각해보니까 이전 버전 기능명세도 2.2 버전인데 왜 수정했는데 v2.2로 그대로 가는거임? v2.3으로 업데이트 안함?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 아니 생각해보니까 이전 버전 기능명세도 2.2 버전인데 왜 수정했는데 v2.2로 그대로 가는거임? v2.3으로 업데이트 안함?, Source Nodes

### Community 144 - "Q: Run uv run pytest -q"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Run uv run pytest -q, Source Nodes

### Community 145 - "CallCounter"
Cohesion: 0.29
Nodes (5): CallCounter, fake_ai(), _fake_duration(), fixture, 외부 AI caller를 fake로 대체 — 실호출 금지 (Global Constraints).

## Knowledge Gaps
- **229 isolated node(s):** `thisabled-backend`, `변경 사항`, `검증`, `API·기능명세 변경 검수`, `프로젝트` (+224 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **50 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `publish_post()` (4× useful, score=2.974412799) _(code changed — re-verify)_
- `caption_chat_message_job()` (3× useful, score=1.804687392)
- `PublishIn` (2× useful, score=1.49495737)
- `main.py` (2× useful, score=1.479629471) _(code changed — re-verify)_
- `upload_video()` (2× useful, score=1.479455429) _(code changed — re-verify)_
- `save_upload()` (2× useful, score=1.478457336)
- `cleanup_stale_drafts()` (2× useful, score=1.478457336)
- `UiMode` (2× useful, score=1.477761898)
- `user_features()` (2× useful, score=1.477761898) _(code changed — re-verify)_

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `blocks.py`, `posts.py`, `v1/comm.py`, `match.py`, `StrictRequest`, `oauth.py`, `services/chat.py`, `config.py`, `v1/auth.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `StrictRequest` connect `StrictRequest` to `blocks.py`, `User`, `config.py`, `v1/comm.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `register()` connect `register` to `test_safe.py`, `test_notifications.py`, `test_match.py`, `test_ws.py`, `test_friends.py`, `conftest.py`, `services/chat.py`, `test_chat.py`, `test_auth.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 62 inferred relationships involving `StrictRequest` (e.g. with `HintsOut` and `PostIn`) actually correct?**
  _`StrictRequest` has 62 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `User` (e.g. with `callback()` and `refresh()`) actually correct?**
  _`User` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thisabled-backend`, `변경 사항`, `검증` to the rest of the system?**
  _229 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `posts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08942307692307692 - nodes in this community are weakly interconnected._