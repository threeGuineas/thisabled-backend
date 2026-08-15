# Graph Report - thisabled-backend  (2026-08-15)

## Corpus Check
- 141 files · ~69,109 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1394 nodes · 3313 edges · 153 communities (97 shown, 56 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 257 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a3c6da84`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- users.py
- v1/auth.py
- posts.py
- ai_media.py
- ai_result_cache 테이블(미디어 해시 캐싱)
- friends.py
- storage.py
- v1/chat.py
- test_config.py
- test_media.py
- quota.py
- Q: 다 구현해줘 & 전체적으로 리팩토링도 필요할거같아 더 깔끔하고 체계적이고 직관적이게 & 또한 전체적으로 결함 탐색+보강이 필요해보이넹 & 지금까지 한것들 커밋들 브랜치 따로 영역에 맞게 분류해서 작업해줘
- StrictRequest
- test_withdrawal.py
- safe_grooming_eval.py
- 채팅 읽음 상태 설계
- ThisAbled API 명세 요약 (v2.3)
- Base
- match.py
- test_chat.py
- ThisAbled — Backend
- test_friends.py
- test_auth.py
- services/comm.py
- Q: 친구 추천 부분도 로딩이 안되는 문제가 있다고 하는데 확인 부탁함
- Q: 피그마 기준으로 게시물 카테고리 포함해서 누락된 백엔드 영역 기능 사항들 점검해줘
- Global Constraints
- SAFE 그루밍 평가 설계
- MATCH-02 추천 입력
- session.py
- test_safe.py
- ThisAbled 기능 명세서 v2.3
- v1/media.py
- register
- fake_ai
- notifications.py
- test_ws.py
- main.py
- SAFE 이진 v6 배포 검증
- 14. 발달장애인 모드 및 AI 소통 코치
- 7. 피드·게시물·댓글
- 10. 1:1 채팅
- generate_caption
- SAFE 최신 호환 서빙 재평가
- 11. AI 안심 채팅
- 1. 서비스 개요
- 4. 사용자 정책
- relations.py
- media_probe.py
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
- _post
- 17. 외부 AI 사용 및 데이터 처리 원칙
- 6. 회원가입 및 계정
- Q: 자막 생성 때문에
- SafetyUnavailable
- Chat Read Status Implementation Plan
- caption_errors.py
- Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?
- Q: 백엔드 핵심 소스코드 2개와 설명
- env.py
- FakeMatch
- CHAT-05 음성·영상 통화 시그널링 설계
- 13. 청각장애인 모드
- async_sessionmaker
- 18. 기술 구성
- 19. 비기능 요구사항
- CaptionTranscriptionError
- 5. 공통 화면 구조
- 9. 친구·차단
- test_schema.py
- AsyncSession
- BackgroundTasks
- Q: 아니 생각해보니까 이전 버전 기능명세도 2.2 버전인데 왜 수정했는데 v2.2로 그대로 가는거임? v2.3으로 업데이트 안함?
- Q: Run uv run pytest -q
- datetime
- delete
- get
- patch
- Any
- FastAPI
- model_validator
- fixture

## God Nodes (most connected - your core abstractions)
1. `User` - 68 edges
2. `register()` - 64 edges
3. `auth_header()` - 61 edges
4. `StrictRequest` - 55 edges
5. `_Redis` - 51 edges
6. `_post()` - 36 edges
7. `ChatMessage` - 31 edges
8. `Base` - 29 edges
9. `_room()` - 27 edges
10. `send_media()` - 26 edges

## Surprising Connections (you probably didn't know these)
- `test_cleanup_deletes_stale_drafts()` --indirect_call--> `Post`  [INFERRED]
  tests/test_media.py → app/models/post.py
- `test_photo_post_gets_description_on_publish()` --indirect_call--> `PostMedia`  [INFERRED]
  tests/test_media.py → app/models/post.py
- `test_vision_quota_exceeded_publishes_without_description()` --indirect_call--> `PostMedia`  [INFERRED]
  tests/test_media.py → app/models/post.py
- `test_normalize_pair_orders_by_uuid()` --calls--> `normalize_pair()`  [EXTRACTED]
  tests/test_age.py → app/core/pairs.py
- `test_withdraw_anonymize_keeps_posts_and_chat()` --indirect_call--> `ChatMessage`  [INFERRED]
  tests/test_withdrawal.py → app/models/chat.py

## Import Cycles
- None detected.

## Communities (153 total, 56 thin omitted)

### Community 0 - "users.py"
Cohesion: 0.08
Nodes (60): me(), _me_out(), patch_me(), patch_settings(), public_profile(), put_mode(), put_tags(), AsyncSession (+52 more)

### Community 1 - "v1/auth.py"
Cohesion: 0.10
Nodes (39): authorize(), callback(), _frontend_redirect(), logout(), _oauth_state_key(), AsyncSession, get, UUID (+31 more)

### Community 2 - "posts.py"
Cohesion: 0.09
Nodes (67): _author_out(), _blocked_ids_subq(), caption_status(), _comment_out(), _contains_pattern(), create_comment(), create_post(), _cursor_position() (+59 more)

### Community 3 - "ai_media.py"
Cohesion: 0.12
Nodes (31): PostMedia, 게시물 미디어 (사진≤3·영상 1개는 앱 검증). VISION 설명·CAPTION 자막 부착., _acquire_caption_lock(), caption_chat_message_job(), caption_post_media_job(), describe_chat_message_job(), describe_post_media_job(), file_path_from_url() (+23 more)

### Community 5 - "friends.py"
Cohesion: 0.29
Nodes (18): accept_request(), _author(), cancel_request(), decline_request(), _get_pending(), list_friends(), list_requests(), AsyncSession (+10 more)

### Community 6 - "storage.py"
Cohesion: 0.23
Nodes (12): content_type_from_path(), delete_upload(), _ext_from_content_type(), Path, Protocol, STT multipart에 파일 확장자와 일치하는 실제 MIME을 제공한다., Save file locally and return the public URL path., 업로드를 메모리에 통째로 올리지 않고 저장하며 크기와 SHA-256을 계산한다. (+4 more)

### Community 7 - "v1/chat.py"
Cohesion: 0.05
Nodes (121): accept_request(), _author(), create_room(), get_call(), _get_my_room(), _latest_messages(), list_messages(), list_requests() (+113 more)

### Community 8 - "test_config.py"
Cohesion: 0.16
Nodes (11): Settings, BaseSettings, _conn(), 테스트 전용 DB만 허용한다. 명시값이 없으면 현재 DB명에 `_test`를 붙인다., _test_database_url(), v2.1 명세 고정값이 Settings에 반영되어 있는지 검증., docker compose env_file은 POSTGRES_PASSWORD/REDIS_PASSWORD도 컨테이너 프로세스에 노출한다. 이…, CI처럼 Docker 볼륨이 없는 환경에서도 테스트 수집 전 app import가 성공해야 한다. (+3 more)

### Community 9 - "test_media.py"
Cohesion: 0.12
Nodes (10): PostMedia, VISION-01 사진 설명 · CAPTION-01 영상 자막 · VIS-03 음성 입력 · 24h 드래프트 청소., 새 Starlette에서는 응답 본문 뒤 background task가 별도 스케줄될 수 있어 완료를 기다린다., test_cleanup_deletes_stale_drafts(), test_image_upload_limit_3(), test_photo_post_gets_description_on_publish(), test_same_image_hash_uses_cache(), test_vision_quota_exceeded_publishes_without_description() (+2 more)

### Community 10 - "quota.py"
Cohesion: 0.12
Nodes (32): consume_vision(), 일 20회·분 5회 동시 검증 — 분 한도 초과 시 일 카운터 롤백., caption_global_key(), caption_key(), caption_refund_marker(), consume_caption(), consume_caption_retry_attempt(), _minute() (+24 more)

### Community 11 - "Q: 다 구현해줘 & 전체적으로 리팩토링도 필요할거같아 더 깔끔하고 체계적이고 직관적이게 & 또한 전체적으로 결함 탐색+보강이 필요해보이넹 & 지금까지 한것들 커밋들 브랜치 따로 영역에 맞게 분류해서 작업해줘"
Cohesion: 0.50
Nodes (3): Answer, Outcome, Q: 다 구현해줘 & 전체적으로 리팩토링도 필요할거같아 더 깔끔하고 체계적이고 직관적이게 & 또한 전체적으로 결함 탐색+보강이 필요해보이넹 & 지금까지 한것들 커밋들 브랜치 따로 영역에 맞게 분류해서 작업해줘

### Community 12 - "StrictRequest"
Cohesion: 0.15
Nodes (37): CallKind, CallSignalType, CallCreateIn, CallOut, CallSignalIn, CallSignalOut, MessageIn, MessageListOut (+29 more)

### Community 13 - "test_withdrawal.py"
Cohesion: 0.07
Nodes (27): Post, 게시물 (POST-01). 텍스트·사진=즉시 published, 영상=processing 드래프트로 시작., §15: 탈퇴 후 30일 재가입 제한 판정용. users 행은 hard delete하고 여기에만 흔적., WithdrawnSocial, get_provider(), GoogleProvider, _http(), KakaoProvider (+19 more)

### Community 14 - "safe_grooming_eval.py"
Cohesion: 0.24
Nodes (16): test_fixture_contains_detection_and_boundary_cases(), test_fixture_rows_match_case_schema(), test_invalid_case_is_rejected(), test_invalid_verdict_is_error_not_safe(), test_summarize_reports_recall_fnr_fpr_and_subgroups(), evaluate(), _group_metrics(), load_cases() (+8 more)

### Community 15 - "채팅 읽음 상태 설계"
Cohesion: 0.22
Nodes (8): API와 실시간 이벤트, 대안과 결정, 데이터 모델, 목표, 범위와 용어, 안전성과 일관성, 채팅 읽음 상태 설계, 테스트

### Community 16 - "ThisAbled API 명세 요약 (v2.3)"
Cohesion: 0.18
Nodes (10): auth (ACC-01/02), chat (CHAT-01~05 · SAFE-01~05), comm (COMM-01~05), friends / blocks (FRIEND-01/02 · BLOCK-01), media (VISION-01 · CAPTION-01 · VIS-03), notifications (§16) / ws, posts / feed (FEED-01 · POST-01~03), recommendations (MATCH) (+2 more)

### Community 17 - "Base"
Cohesion: 0.15
Nodes (17): Base, AiResultCache, Notification, 알림 (§16). WS 푸시와 병행 저장., 동일 미디어 해시 캐싱 (VISION-01·CAPTION-01 중복 호출 방지, 비용 방어)., Friendship, 양방향 친구 관계 (FRIEND-02). 정규화 쌍: user_a < user_b., ForbiddenNickname (+9 more)

### Community 18 - "match.py"
Cohesion: 0.17
Nodes (19): AsyncSession, BaseModel, get, RecommendationListOut, RecommendationOut, recommendations(), friend_requests. declined+responded_at은 30일 추천 제외 근거(MATCH-03)., RequestStatus (+11 more)

### Community 19 - "test_chat.py"
Cohesion: 0.23
Nodes (19): _describe_fake(), make_friends(), CHAT-01 친구 채팅 · CHAT-02 비친구 요청 · 미디어 제한 (§4.5)., _room(), test_chat_caption_failure_exposes_stable_code_without_recall(), test_chat_text_is_trimmed_and_limited(), test_chat_video_gets_caption_and_notifies_both_users(), test_friend_chat_roundtrip() (+11 more)

### Community 20 - "ThisAbled — Backend"
Cohesion: 0.15
Nodes (12): DB 스키마 (v3), graphify, Ralph 루프 (선택), ThisAbled — Backend, 기술 스택, 데드라인, 링크, 명령어 (+4 more)

### Community 21 - "test_friends.py"
Cohesion: 0.44
Nodes (9): _pair(), FRIEND-01/02 친구 요청·관리 · BLOCK-01 차단., _request(), test_block_removes_friendship_and_hides_everything(), test_cancel_only_by_sender(), test_decline_records_and_duplicate_pending_rejected(), test_request_accept_creates_mutual_friendship(), test_self_request_rejected() (+1 more)

### Community 22 - "test_auth.py"
Cohesion: 0.08
Nodes (37): get_redis(), get_redis_client(), 현재 이벤트 루프 전용 클라이언트. asyncio Redis 연결을 다른 루프에서 재사용하면 Future/transport가 깨지므로…, FastAPI 의존성. 테스트에서 override 가능하도록 분리., callback_params(), 콜백 302 리다이렉트(Location=FRONTEND_URL?…)의 쿼리 파라미터 → 단일값 dict., ACC-01/02 — 소셜 OAuth 전용 인증 (mock 제공자)., _signup_token() (+29 more)

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

### Community 29 - "session.py"
Cohesion: 0.13
Nodes (22): BlockedOut, create_block(), list_blocks(), AsyncSession, BaseModel, delete, get, UUID (+14 more)

### Community 30 - "test_safe.py"
Cohesion: 0.35
Nodes (11): _send(), _friend_room(), SAFE-01~05 — 동기 분석·블러·내용 보기·성능저하 모드·관계 단위 전송 제한., §18.3: 복구 후 재분석 — flagged면 소급 블러 + 수신자 알림., 수신자가 '내용 보기'를 실행한 메시지도 누적 집계에 포함 (SAFE-05-6)., test_block_overrides_restriction(), test_degraded_mode_friend_vs_request(), test_flagged_message_blurred_until_reveal() (+3 more)

### Community 31 - "ThisAbled 기능 명세서 v2.3"
Cohesion: 0.20
Nodes (9): 15. 마이페이지·설정, 16. 알림, 20. 핵심 인수 조건, 21. MVP 이후 계획, 2. 핵심 기능명, 3.1 포함, 3.2 제외 및 후속 범위, 3. MVP 범위 (+1 more)

### Community 32 - "v1/media.py"
Cohesion: 0.14
Nodes (20): async_sessionmaker, AsyncSession, BackgroundTasks, UploadFile, 미디어 업로드 — 사진(≤3장) · 영상(드래프트+자막 시작) · VIS-03 음성 입력., VIS-03 음성 입력 — 결과는 입력란 삽입용. 자동 게시하지 않는다 (§20-4)., 사진 업로드 (post 미연결) — POST /posts 의 media_ids로 연결한다., 영상 첨부 = processing 내부 드래프트 생성 + 자막 생성 즉시 시작 (POST-01·CAPTION-01). FE 길이는 빠른 거부용… (+12 more)

### Community 33 - "register"
Cohesion: 0.15
Nodes (29): auth_header(), mock OAuth 가입 헬퍼 → {access_token, user_id, ...}., register(), test_post_comments_hide_blocked_post(), test_post_comments_use_post_and_latest_10_comments(), test_simplify_and_complete(), MATCH — 후보 제외 규칙은 백엔드 강제, 점수·사유는 모델 서버 (mock/fake)., 도메인 default는 MATCH 서버가 허용하는 중립값으로 직렬화한다. (+21 more)

### Community 34 - "fake_ai"
Cohesion: 0.29
Nodes (5): fixture, CallCounter, fake_ai(), _fake_duration(), 외부 AI caller를 fake로 대체 — 실호출 금지 (Global Constraints).

### Community 35 - "notifications.py"
Cohesion: 0.36
Nodes (9): list_notifications(), mark_read(), NotificationListOut, NotificationOut, AsyncSession, BaseModel, get, ReadIn (+1 more)

### Community 36 - "test_ws.py"
Cohesion: 0.15
Nodes (26): WS /api/v1/ws?token=<access> — 새 메시지·알림·통화 시그널 실시간 푸시. 인증은 JWT 검증만으로 처리(DB…, _relay(), ws_endpoint(), 실시간 이벤트 — Redis pub/sub 팬아웃 (다중 워커에서도 사용자별 채널로 전달). event 형식: {"type":…, user_channel(), heartbeat(), mark_offline(), mark_online() (+18 more)

### Community 37 - "main.py"
Cohesion: 0.06
Nodes (39): Any, health(), HealthOut, BaseModel, get, close_redis_client(), 현재 워커 이벤트 루프의 연결 풀을 애플리케이션 종료 시 정리한다., add_security_headers() (+31 more)

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

### Community 42 - "generate_caption"
Cohesion: 0.43
Nodes (8): _cache_get(), _cache_put(), CaptionGenerationResult, describe_image(), generate_caption(), AsyncSession, 사진 설명 생성. 실패·한도 초과 시 None (게시·전송은 정상 유지)., 자막 세그먼트 생성. 쿼터는 업로드 시점에 이미 차감 — 실패(재시도 소진) 시 복원.

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

### Community 47 - "relations.py"
Cohesion: 0.26
Nodes (11): normalize_pair(), UUID, 사용자 쌍 정규화. friendships·chat_rooms는 (작은 UUID, 큰 UUID) 순으로 저장한다., Block, 차단 (BLOCK-01). 게시물·프로필·요청·채팅·추천 접점을 상호 제거., are_friends(), block_user(), AsyncSession (+3 more)

### Community 48 - "media_probe.py"
Cohesion: 0.38
Nodes (6): get_video_probe(), InvalidVideo, probe_video_duration(), Exception, Path, 서버가 직접 영상 컨테이너와 재생 시간을 검증한다.

### Community 50 - "MATCH v2 배포 성능 평가"
Cohesion: 0.20
Nodes (9): 1. 기동 및 계약, 2.1 배포 번들 저장 지표, 2.2 배포 모델 독립 재평가, 2. 랭킹 품질, 3. 공정성 및 활동량 편향, 4. 실서버 지연, 5. 운영 관찰사항, 6. 최종 판정 (+1 more)

### Community 54 - "config.py"
Cohesion: 0.33
Nodes (5): generate_description(), _get_client(), AsyncOpenAI, GPT-4o Vision 이미지 해설 서비스 (F02_S04 시각장애 모드). 엔드포인트는…, 이미지 바이트 → 한국어 해설 텍스트. (실제 GPT-4o 호출)

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
Cohesion: 0.16
Nodes (14): _BorrowedSession, client(), _force_oauth_mock(), _isolate_upload_directory(), AsyncClient, fixture, 테스트 공용 픽스처. 각 테스트는 단일 커넥션 위의 외부 트랜잭션에서 실행되고 끝나면 롤백된다. 앱 코드가 `await db.commit()`…, .env의 실키·OAUTH_MOCK=false는 배포용 — 테스트는 항상 mock 제공자로 결정론적으로 실행한다. 개별… (+6 more)

### Community 116 - "_post"
Cohesion: 0.10
Nodes (24): Features, health(), BaseModel, get, match-model mock — SBERT+LightGBM 모델 서버가 오기 전 자리 지킴이. 계약: POST /score {me,…, score(), ScoreIn, analyze() (+16 more)

### Community 117 - "17. 외부 AI 사용 및 데이터 처리 원칙"
Cohesion: 0.40
Nodes (5): 17.1 자체 처리 (외부 미전송), 17.2 외부 AI API 사용 (가입 시 필수 고지), 17.3 공통 처리 원칙, 17.4 관리자 기능, 17. 외부 AI 사용 및 데이터 처리 원칙

### Community 118 - "6. 회원가입 및 계정"
Cohesion: 0.40
Nodes (5): 6. 회원가입 및 계정, ACC-01 회원가입 (소셜 로그인), ACC-02 로그인·로그아웃, ACC-03 프로필, TAG-01 관심사 태그 체계 (정본)

### Community 120 - "Q: 자막 생성 때문에"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 자막 생성 때문에, Source Nodes

### Community 121 - "SafetyUnavailable"
Cohesion: 0.14
Nodes (14): get_safety_client(), Exception, 모델 서버 장애·지연 — 친구 텍스트는 unanalyzed 전달, 비친구는 pending 보류., → 'safe' | 'flagged'. 미성년 수신자는 민감(낮은) 임계값 (§4.5)., FastAPI 의존성 — 테스트에서 fake로 override., SafetyUnavailable, FakeSafety, fixture (+6 more)

### Community 122 - "Chat Read Status Implementation Plan"
Cohesion: 0.25
Nodes (7): Chat Read Status Implementation Plan, File Structure, Global Constraints, Plan Self-Review, Task 1: Write failing behavior tests, Task 2: Persist and calculate the cursor, Task 3: Expose, document, verify, and commit

### Community 126 - "caption_errors.py"
Cohesion: 0.47
Nodes (5): caption_failure_details(), caption_failure_state(), CaptionFailureDetails, CAPTION-01 실패 코드와 프론트 표시용 안전한 메시지., failed 상태에만 안정적인 코드·표시 문구·재시도 가능 여부를 노출한다.

### Community 127 - "Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?, Source Nodes

### Community 128 - "Q: 백엔드 핵심 소스코드 2개와 설명"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 백엔드 핵심 소스코드 2개와 설명, Source Nodes

### Community 129 - "env.py"
Cohesion: 0.60
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

### Community 130 - "FakeMatch"
Cohesion: 0.40
Nodes (3): FakeMatch, match(), fixture

### Community 131 - "CHAT-05 음성·영상 통화 시그널링 설계"
Cohesion: 0.29
Nodes (6): API와 이벤트, CHAT-05 음성·영상 통화 시그널링 설계, 검증, 목표와 경계, 오류 계약, 정책

### Community 132 - "13. 청각장애인 모드"
Cohesion: 0.50
Nodes (4): 13. 청각장애인 모드, HEAR-01 기본 UI, HEAR-02 영상 자막, HEAR-03 알림

### Community 134 - "18. 기술 구성"
Cohesion: 0.50
Nodes (4): 18.1 웹 서비스, 18.2 AI 모듈, 18.3 설계 원칙, 18. 기술 구성

### Community 135 - "19. 비기능 요구사항"
Cohesion: 0.50
Nodes (4): 19.1 접근성, 19.2 개인정보·보안, 19.3 AI 품질, 19. 비기능 요구사항

### Community 136 - "CaptionTranscriptionError"
Cohesion: 0.16
Nodes (17): CaptionTranscriptionError, RuntimeError, 호출자가 자동 재시도 여부를 판단할 수 있는 자막 처리 오류., _extract_audio_to_m4a(), _get_client(), _normalize_segments(), Any, AsyncOpenAI (+9 more)

### Community 137 - "5. 공통 화면 구조"
Cohesion: 0.50
Nodes (4): 5.1 주요 화면, 5.2 UI 모드 전환, 5.3 기본 모드 (GEN-01, 신설), 5. 공통 화면 구조

### Community 138 - "9. 친구·차단"
Cohesion: 0.50
Nodes (4): 9. 친구·차단, BLOCK-01 사용자 차단, FRIEND-01 친구 요청, FRIEND-02 친구 관리

### Community 139 - "test_schema.py"
Cohesion: 0.29
Nodes (3): 스키마 v3 baseline 정합 검증 (설계: docs/superpowers/specs/2026-07-05-v2_1-refactor-…, 탈퇴 익명화(§15): 게시물·댓글·채팅 발신자는 SET NULL 가능해야 한다., test_anonymizable_fks_nullable()

### Community 143 - "Q: 아니 생각해보니까 이전 버전 기능명세도 2.2 버전인데 왜 수정했는데 v2.2로 그대로 가는거임? v2.3으로 업데이트 안함?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 아니 생각해보니까 이전 버전 기능명세도 2.2 버전인데 왜 수정했는데 v2.2로 그대로 가는거임? v2.3으로 업데이트 안함?, Source Nodes

### Community 144 - "Q: Run uv run pytest -q"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Run uv run pytest -q, Source Nodes

## Knowledge Gaps
- **225 isolated node(s):** `auth (ACC-01/02)`, `users (ACC-03 · TAG-01 · §15)`, `posts / feed (FEED-01 · POST-01~03)`, `media (VISION-01 · CAPTION-01 · VIS-03)`, `friends / blocks (FRIEND-01/02 · BLOCK-01)` (+220 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **56 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `publish_post()` (4× useful, score=3.977918254)
- `caption_chat_message_job()` (3× useful, score=2.41355165)
- `PublishIn` (2× useful, score=1.999325115)
- `main.py` (2× useful, score=1.978825899)
- `upload_video()` (2× useful, score=1.978593139)
- `save_upload()` (2× useful, score=1.97725831)
- `cleanup_stale_drafts()` (2× useful, score=1.97725831)
- `UiMode` (2× useful, score=1.976328246)
- `user_features()` (2× useful, score=1.976328246)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `v1/chat.py` to `v1/media.py`, `v1/auth.py`, `posts.py`, `notifications.py`, `users.py`, `friends.py`, `test_withdrawal.py`, `Base`, `match.py`, `session.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `_Redis` connect `v1/chat.py` to `v1/media.py`, `v1/auth.py`, `ai_media.py`, `test_ws.py`, `friends.py`, `main.py`, `quota.py`, `generate_caption`, `StrictRequest`, `Base`, `test_auth.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `ChatMessage` connect `v1/chat.py` to `test_chat.py`, `Base`, `ai_media.py`, `test_withdrawal.py`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `User` (e.g. with `callback()` and `refresh()`) actually correct?**
  _`User` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 46 inferred relationships involving `StrictRequest` (e.g. with `HintsOut` and `PostIn`) actually correct?**
  _`StrictRequest` has 46 INFERRED edges - model-reasoned connections that need verification._
- **What connects `auth (ACC-01/02)`, `users (ACC-03 · TAG-01 · §15)`, `posts / feed (FEED-01 · POST-01~03)` to the rest of the system?**
  _225 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `users.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07596153846153846 - nodes in this community are weakly interconnected._