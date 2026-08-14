# Graph Report - thisabled-backend  (2026-08-15)

## Corpus Check
- 125 files · ~62,781 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1247 nodes · 2971 edges · 139 communities (84 shown, 55 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 180 edges (avg confidence: 0.67)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bda0c116`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- match.py
- users.py
- User
- ai_media.py
- ai_result_cache 테이블(미디어 해시 캐싱)
- friends.py
- generate_caption
- register
- stt.py
- signup
- quota.py
- match_model.py
- v1/comm.py
- models/user.py
- safe_grooming_eval.py
- 채팅 읽음 상태 설계
- ThisAbled API 명세 요약 (v2.2)
- MATCH-02 추천 입력
- test_auth.py
- config.py
- ThisAbled — Backend
- ThisAbled 기능 명세서 v2.2
- v1/auth.py
- services/comm.py
- Q: 친구 추천 부분도 로딩이 안되는 문제가 있다고 하는데 확인 부탁함
- Q: 피그마 기준으로 게시물 카테고리 포함해서 누락된 백엔드 영역 기능 사항들 점검해줘
- Global Constraints
- SAFE 그루밍 평가 설계
- 14. 발달장애인 모드 및 AI 소통 코치
- 7. 피드·게시물·댓글
- test_users.py
- 11. AI 안심 채팅
- 1. 서비스 개요
- get_redis_client
- 4. 사용자 정책
- 10. 1:1 채팅
- 12. 시각장애인 모드
- main.py
- SAFE 이진 v6 배포 검증
- 17. 외부 AI 사용 및 데이터 처리 원칙
- 6. 회원가입 및 계정
- 0. 문서 정보
- v1/chat.py
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
- test_chat.py
- _Redis
- SAFE 그루밍 평가 결과
- test_withdrawal.py
- fake_ai
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
- test_schema.py
- Q: ㅇㅇ 수정 ㄱㄱ 그리고 [api 문서](https://ideal-macmini.tail72b898.ts.net/docs) 자세하게, 결함 없게 구체적으로 아주 친절하게 패치해줘 프론트엔드가 곤란하지 않도록
- Q: 영상 자막 부분 기능 감사해줘
- thisabled-backend
- Q: ㅇㅋ 결함들 해결 방안 추천해줘
- Q: 영상 자막 결함 해결 방안 구현
- conftest.py
- vision.py
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
- test_ws.py
- Google OAuth Setup
- Kakao OAuth Setup
- OAuth Mock Provider (dev)
- OAuth Redirect URI Decision
- Definition of Done 체크리스트
- Redis TTL 호출 한도 카운터(vision·caption)
- users 테이블
- test_friends.py
- session.py
- safety_model.py
- test_notifications.py
- env.py
- nickname.py
- Chat Read Status Implementation Plan
- _frontend_redirect
- Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?
- Q: 백엔드 핵심 소스코드 2개와 설명
- get_describe_caller
- get_text_transcriber
- v1/media.py
- delete
- get
- patch
- UUID
- Any
- FastAPI
- BaseModel

## God Nodes (most connected - your core abstractions)
1. `User` - 83 edges
2. `register()` - 66 edges
3. `auth_header()` - 63 edges
4. `_Redis` - 46 edges
5. `_post()` - 33 edges
6. `ChatMessage` - 31 edges
7. `send_media()` - 26 edges
8. `PostCategory` - 23 edges
9. `ChatRoom` - 23 edges
10. `ThisAbled 기능 명세서 v2.2` - 23 edges

## Surprising Connections (you probably didn't know these)
- `test_mode_change_records_history()` --indirect_call--> `UserModeHistory`  [INFERRED]
  tests/test_users.py → app/models/user.py
- `test_withdraw_anonymize_keeps_posts_and_chat()` --indirect_call--> `User`  [INFERRED]
  tests/test_withdrawal.py → app/models/user.py
- `test_rejoin_blocked_within_30_days()` --indirect_call--> `WithdrawnSocial`  [INFERRED]
  tests/test_auth.py → app/models/user.py
- `test_withdraw_anonymize_keeps_posts_and_chat()` --indirect_call--> `WithdrawnSocial`  [INFERRED]
  tests/test_withdrawal.py → app/models/user.py
- `test_withdraw_anonymize_keeps_posts_and_chat()` --indirect_call--> `ChatMessage`  [INFERRED]
  tests/test_withdrawal.py → app/models/chat.py

## Import Cycles
- None detected.

## Communities (139 total, 55 thin omitted)

### Community 0 - "match.py"
Cohesion: 0.09
Nodes (33): AsyncSession, BaseModel, get, RecommendationListOut, RecommendationOut, recommendations(), age_band(), full_age() (+25 more)

### Community 1 - "users.py"
Cohesion: 0.08
Nodes (53): me(), _me_out(), patch_me(), patch_settings(), public_profile(), put_mode(), put_tags(), AsyncSession (+45 more)

### Community 2 - "User"
Cohesion: 0.10
Nodes (63): _author_out(), _blocked_ids_subq(), caption_status(), _comment_out(), _contains_pattern(), create_comment(), create_post(), _cursor_position() (+55 more)

### Community 3 - "ai_media.py"
Cohesion: 0.12
Nodes (32): content_type_from_path(), STT multipart에 파일 확장자와 일치하는 실제 MIME을 제공한다., PostMedia, 게시물 미디어 (사진≤3·영상 1개는 앱 검증). VISION 설명·CAPTION 자막 부착., _acquire_caption_lock(), caption_chat_message_job(), caption_post_media_job(), describe_chat_message_job() (+24 more)

### Community 5 - "friends.py"
Cohesion: 0.08
Nodes (53): BlockedOut, create_block(), list_blocks(), AsyncSession, BaseModel, delete, get, UUID (+45 more)

### Community 6 - "generate_caption"
Cohesion: 0.52
Nodes (7): _cache_get(), _cache_put(), describe_image(), generate_caption(), AsyncSession, 사진 설명 생성. 실패·한도 초과 시 None (게시·전송은 정상 유지)., 자막 세그먼트 생성. 쿼터는 업로드 시점에 이미 차감 — 실패(재시도 소진) 시 복원.

### Community 7 - "register"
Cohesion: 0.12
Nodes (42): Block, 차단 (BLOCK-01). 게시물·프로필·요청·채팅·추천 접점을 상호 제거., RuntimeError, auth_header(), mock OAuth 가입 헬퍼 → {access_token, user_id, ...}., register(), test_post_comments_hide_blocked_post(), test_post_comments_use_post_and_latest_10_comments() (+34 more)

### Community 8 - "stt.py"
Cohesion: 0.23
Nodes (11): _extract_audio_to_m4a(), _get_client(), AsyncOpenAI, Path, OpenAI Whisper STT 서비스 (F02_S05 음성 댓글 / 자막). 엔드포인트는 `stt.transcribe(...)` 를…, 오디오 바이트 → 한국어 전사 텍스트. (실제 Whisper 호출, VIS-03 음성 입력), 최대 200MB 영상을 STT 상한 안의 단일 채널 M4A 음성으로 정규화한다., 영상/오디오 → 자막 세그먼트 [{start, end, text}] (CAPTION-01). (+3 more)

### Community 9 - "signup"
Cohesion: 0.19
Nodes (19): callback(), logout(), AsyncSession, get, UUID, refresh(), _set_refresh_cookie(), signup() (+11 more)

### Community 10 - "quota.py"
Cohesion: 0.12
Nodes (32): consume_vision(), 일 20회·분 5회 동시 검증 — 분 한도 초과 시 일 카운터 롤백., caption_global_key(), caption_key(), caption_refund_marker(), consume_caption(), consume_caption_retry_attempt(), _minute() (+24 more)

### Community 11 - "match_model.py"
Cohesion: 0.32
Nodes (7): Features, health(), BaseModel, get, match-model mock — SBERT+LightGBM 모델 서버가 오기 전 자리 지킴이. 계약: POST /score {me,…, score(), ScoreIn

### Community 12 - "v1/comm.py"
Cohesion: 0.15
Nodes (33): _coach(), complete(), hints(), HintsOut, _post_context(), PostIn, AsyncSession, BaseModel (+25 more)

### Community 13 - "models/user.py"
Cohesion: 0.07
Nodes (21): 소셜 계정 연결 (ACC-01). 사용자 1명이 복수 제공자 연결 가능., §15: 탈퇴 후 30일 재가입 제한 판정용. users 행은 hard delete하고 여기에만 흔적., SocialIdentity, WithdrawnSocial, get_provider(), GoogleProvider, _http(), KakaoProvider (+13 more)

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

### Community 18 - "test_auth.py"
Cohesion: 0.10
Nodes (29): callback_params(), 콜백 302 리다이렉트(Location=FRONTEND_URL?…)의 쿼리 파라미터 → 단일값 dict., ACC-01/02 — 소셜 OAuth 전용 인증 (mock 제공자)., _signup_token(), test_callback_new_user_redirects_with_signup_token(), test_existing_user_callback_logs_in(), test_invalid_mock_code_redirects_with_error(), test_refresh_rotates_access_token() (+21 more)

### Community 19 - "config.py"
Cohesion: 0.16
Nodes (9): health(), HealthOut, BaseModel, get, Settings, BaseSettings, v2.1 명세 고정값이 Settings에 반영되어 있는지 검증., docker compose env_file은 POSTGRES_PASSWORD/REDIS_PASSWORD도 컨테이너 프로세스에 노출한다. 이… (+1 more)

### Community 20 - "ThisAbled — Backend"
Cohesion: 0.15
Nodes (12): DB 스키마 (v3), graphify, Ralph 루프 (선택), ThisAbled — Backend, 기술 스택, 데드라인, 링크, 명령어 (+4 more)

### Community 21 - "ThisAbled 기능 명세서 v2.2"
Cohesion: 0.20
Nodes (9): 15. 마이페이지·설정, 16. 알림, 20. 핵심 인수 조건, 21. MVP 이후 계획, 2. 핵심 기능명, 3.1 포함, 3.2 제외 및 후속 범위, 3. MVP 범위 (+1 more)

### Community 22 - "v1/auth.py"
Cohesion: 0.33
Nodes (11): authorize(), ACC-01/02 — 소셜 OAuth 전용 인증. 흐름: authorize → 제공자 로그인 → callback → FRONTEND_URL로…, §5.2·GEN-01 — 가입 시 4종 중 하나 필수 선택., UiMode, AccessTokenOut, Agreements, AuthorizeOut, BaseModel (+3 more)

### Community 23 - "services/comm.py"
Cohesion: 0.07
Nodes (24): _collect_strings(), CommUnavailable, get_comm_client(), OpenAICommClient, _plain_text(), COMM — LLM 소통 코치 (외부 API, §17.2 고지 대상). 버튼 실행 시에만 동작(COMM-05). 채팅 컨텍스트는 최근 N개…, FastAPI 의존성 — 테스트에서 fake로 override., 외부 코칭 결과를 안전한 API 응답으로 만들 수 없을 때. (+16 more)

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

### Community 28 - "14. 발달장애인 모드 및 AI 소통 코치"
Cohesion: 0.29
Nodes (7): 14. 발달장애인 모드 및 AI 소통 코치, COMM-01 쉬운 문장 변환, COMM-02 문장 완성, COMM-03 댓글·답장 추천, COMM-04 대화 힌트, COMM-05 데이터 처리 원칙, DEV-01 기본 UI

### Community 29 - "7. 피드·게시물·댓글"
Cohesion: 0.29
Nodes (7): 7. 피드·게시물·댓글, CAPTION-01 영상 자동 자막, FEED-01 홈 피드, POST-01 게시물 작성, POST-02 수정·삭제, POST-03 좋아요·댓글, VISION-01 AI 사진 설명

### Community 31 - "11. AI 안심 채팅"
Cohesion: 0.33
Nodes (6): 11. AI 안심 채팅, SAFE-01 분석 원칙과 전달 타이밍, SAFE-02 탐지 범위, SAFE-03 사용자 표시, SAFE-04 내부 위험 점수, SAFE-05 관계 단위 자동 전송 제한 (신설)

### Community 32 - "1. 서비스 개요"
Cohesion: 0.33
Nodes (6): 1.1 서비스명, 1.2 서비스 정의 (한 문장), 1.3 서비스 비전, 1.4 해결하려는 문제, 1.5 핵심 사용자 경험, 1. 서비스 개요

### Community 33 - "get_redis_client"
Cohesion: 0.50
Nodes (4): get_redis_client(), 현재 이벤트 루프 전용 클라이언트. asyncio Redis 연결을 다른 루프에서 재사용하면 Future/transport가 깨지므로…, §18.3: 모델 복구 감지용 주기 재분석 (unanalyzed·pending 텍스트)., _reanalyze_job()

### Community 34 - "4. 사용자 정책"
Cohesion: 0.33
Nodes (6): 4.1 가입 대상, 4.2 장애인 자격 확인, 4.3 복합장애, 4.4 콘텐츠 공개, 4.5 미성년자 보호 (신설), 4. 사용자 정책

### Community 35 - "10. 1:1 채팅"
Cohesion: 0.40
Nodes (5): 10. 1:1 채팅, CHAT-01 친구 채팅, CHAT-02 비친구 메시지 요청, CHAT-03 채팅 상태, CHAT-04 읽음·안읽음 표시 (신설)

### Community 36 - "12. 시각장애인 모드"
Cohesion: 0.40
Nodes (5): 12. 시각장애인 모드, VIS-01 기본 UI, VIS-02 스크린리더, VIS-03 음성 입력, VIS-04 상태 안내

### Community 37 - "main.py"
Cohesion: 0.09
Nodes (36): Any, WS /api/v1/ws?token=<access> — 새 메시지·알림 실시간 푸시. 인증은 JWT 검증만으로 처리(DB 미조회)해 연결…, _relay(), ws_endpoint(), get_redis(), FastAPI 의존성. 테스트에서 override 가능하도록 분리., lifespan(), FastAPI (+28 more)

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

### Community 42 - "v1/chat.py"
Cohesion: 0.06
Nodes (90): accept_request(), _author(), create_room(), _get_my_room(), _latest_messages(), list_messages(), list_requests(), list_rooms() (+82 more)

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

### Community 54 - "test_chat.py"
Cohesion: 0.17
Nodes (28): _describe_fake(), make_friends(), CHAT-01 친구 채팅 · CHAT-02 비친구 요청 · 미디어 제한 (§4.5)., _room(), _send(), test_chat_video_gets_caption_and_notifies_both_users(), test_friend_chat_roundtrip(), test_media_blocked_in_request_room() (+20 more)

### Community 55 - "_Redis"
Cohesion: 0.17
Nodes (7): _Connection, _Engine, Exception, 헬스체크는 내부 오류를 노출하지 않고 장애 시 HTTP 503을 반환한다., _Redis, test_health_degraded_is_503_and_hides_exception(), test_health_ok()

### Community 63 - "SAFE 그루밍 평가 결과"
Cohesion: 0.40
Nodes (4): SAFE 그루밍 평가 결과, 기존 3a holdout, 신규 합성셋 결과, 진단

### Community 64 - "test_withdrawal.py"
Cohesion: 0.50
Nodes (7): _make_chat(), _make_post(), UUID, §15 회원 탈퇴 — 익명화/삭제 선택, 채팅 보존, 30일 재가입 제한., test_withdraw_anonymize_keeps_posts_and_chat(), test_withdraw_delete_removes_posts(), test_withdraw_invalidates_token_and_blocks_rejoin()

### Community 66 - "fake_ai"
Cohesion: 0.29
Nodes (5): CallCounter, fake_ai(), _fake_duration(), fixture, 외부 AI caller를 fake로 대체 — 실호출 금지 (Global Constraints).

### Community 83 - "test_schema.py"
Cohesion: 0.29
Nodes (3): 스키마 v3 baseline 정합 검증 (설계: docs/superpowers/specs/2026-07-05-v2_1-refactor-…, 탈퇴 익명화(§15): 게시물·댓글·채팅 발신자는 SET NULL 가능해야 한다., test_anonymizable_fks_nullable()

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

### Community 89 - "conftest.py"
Cohesion: 0.15
Nodes (16): _BorrowedSession, client(), _conn(), _force_oauth_mock(), AsyncClient, fixture, 테스트 공용 픽스처. 각 테스트는 단일 커넥션 위의 외부 트랜잭션에서 실행되고 끝나면 롤백된다. 앱 코드가 `await db.commit()`…, .env의 실키·OAUTH_MOCK=false는 배포용 — 테스트는 항상 mock 제공자로 결정론적으로 실행한다. 개별… (+8 more)

### Community 90 - "vision.py"
Cohesion: 0.40
Nodes (5): generate_description(), _get_client(), AsyncOpenAI, GPT-4o Vision 이미지 해설 서비스 (F02_S04 시각장애 모드). 엔드포인트는…, 이미지 바이트 → 한국어 해설 텍스트. (실제 GPT-4o 호출)

### Community 108 - "test_ws.py"
Cohesion: 0.13
Nodes (15): 실시간 이벤트 — Redis pub/sub 팬아웃 (다중 워커에서도 사용자별 채널로 전달). event 형식: {"type":…, user_channel(), FakeSafety, fixture, 돈' 포함 → flagged. fail=True → SafetyUnavailable (§18.3)., safety(), fixture, safety() (+7 more)

### Community 116 - "test_friends.py"
Cohesion: 0.44
Nodes (9): _pair(), FRIEND-01/02 친구 요청·관리 · BLOCK-01 차단., _request(), test_block_removes_friendship_and_hides_everything(), test_cancel_only_by_sender(), test_decline_records_and_duplicate_pending_rejected(), test_request_accept_creates_mutual_friendship(), test_self_request_rejected() (+1 more)

### Community 117 - "session.py"
Cohesion: 0.20
Nodes (15): list_notifications(), mark_read(), NotificationListOut, NotificationOut, AsyncSession, BaseModel, get, ReadIn (+7 more)

### Community 118 - "safety_model.py"
Cohesion: 0.33
Nodes (6): analyze(), AnalyzeIn, health(), BaseModel, get, safety-model mock — AI 팀원의 자체 파인튜닝 안전 모델 서버가 오기 전 자리 지킴이. 계약: POST /analyze…

### Community 119 - "test_notifications.py"
Cohesion: 0.43
Nodes (7): _notis(), §16 알림 — 생성 훅·목록·읽음. WS 푸시는 test_ws에서 검증., test_comment_and_like_notify_author_not_self(), test_disabled_notification_group_is_not_stored(), test_flagged_and_restriction_notify_receiver(), test_friend_request_and_accept_notifications(), test_mark_read()

### Community 120 - "env.py"
Cohesion: 0.60
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

### Community 121 - "nickname.py"
Cohesion: 0.40
Nodes (4): AsyncSession, 닉네임 정책 (ACC-01): 2~12자 한글·영문·숫자, 금칙어·중복 불가., 형식(400) → 금칙어(400) → 중복(409) 순 검증. 통과 시 None., validate_nickname()

### Community 122 - "Chat Read Status Implementation Plan"
Cohesion: 0.25
Nodes (7): Chat Read Status Implementation Plan, File Structure, Global Constraints, Plan Self-Review, Task 1: Write failing behavior tests, Task 2: Persist and calculate the cursor, Task 3: Expose, document, verify, and commit

### Community 126 - "_frontend_redirect"
Cohesion: 0.67
Nodes (3): _frontend_redirect(), 콜백 결과를 프론트 SPA로 302 전달 — 브라우저가 직접 호출하므로 JSON 대신 리다이렉트., RedirectResponse

### Community 127 - "Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?, Source Nodes

### Community 128 - "Q: 백엔드 핵심 소스코드 2개와 설명"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 백엔드 핵심 소스코드 2개와 설명, Source Nodes

### Community 131 - "v1/media.py"
Cohesion: 0.08
Nodes (39): async_sessionmaker, AsyncSession, BackgroundTasks, UploadFile, 미디어 업로드 — 사진(≤3장) · 영상(드래프트+자막 시작) · VIS-03 음성 입력., VIS-03 음성 입력 — 결과는 입력란 삽입용. 자동 게시하지 않는다 (§20-4)., 사진 업로드 (post 미연결) — POST /posts 의 media_ids로 연결한다., 영상 첨부 = processing 내부 드래프트 생성 + 자막 생성 즉시 시작 (POST-01·CAPTION-01). FE 길이는 빠른 거부용… (+31 more)

## Knowledge Gaps
- **198 isolated node(s):** `auth (ACC-01/02)`, `users (ACC-03 · TAG-01 · §15)`, `posts / feed (FEED-01 · POST-01~03)`, `media (VISION-01 · CAPTION-01 · VIS-03)`, `friends / blocks (FRIEND-01/02 · BLOCK-01)` (+193 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **55 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `caption_chat_message_job()` (3× useful, score=2.438879416)
- `save_upload()` (2× useful, score=1.998007622)
- `caption_post_media_job()` (2× useful, score=1.998007622)
- `caption_key()` (2× useful, score=1.998007622)
- `cleanup_stale_drafts()` (2× useful, score=1.998007622)
- `transcribe_segments()` (2× useful, score=1.998007622)
- `recommendations()` (2× useful, score=1.997067798)
- `UiMode` (2× useful, score=1.997067798)
- `user_features()` (2× useful, score=1.997067798)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `match.py`, `users.py`, `test_withdrawal.py`, `v1/media.py`, `friends.py`, `signup`, `v1/chat.py`, `v1/comm.py`, `models/user.py`, `session.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `_post()` connect `register` to `v1/media.py`, `friends.py`, `signup`, `v1/chat.py`, `match_model.py`, `v1/comm.py`, `session.py`, `safety_model.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `_Redis` connect `_Redis` to `get_redis_client`, `User`, `v1/media.py`, `ai_media.py`, `main.py`, `friends.py`, `generate_caption`, `v1/chat.py`, `quota.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `User` (e.g. with `callback()` and `refresh()`) actually correct?**
  _`User` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `auth (ACC-01/02)`, `users (ACC-03 · TAG-01 · §15)`, `posts / feed (FEED-01 · POST-01~03)` to the rest of the system?**
  _198 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `match.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09487179487179487 - nodes in this community are weakly interconnected._
- **Should `users.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07864488808227466 - nodes in this community are weakly interconnected._