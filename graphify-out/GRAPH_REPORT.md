# Graph Report - thisabled-backend  (2026-08-15)

## Corpus Check
- 123 files · ~61,371 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1212 nodes · 2941 edges · 118 communities (72 shown, 46 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 198 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c92c59a8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- scheduler.py
- users.py
- User
- _Redis
- ai_result_cache 테이블(미디어 해시 캐싱)
- friends.py
- ai_media.py
- register
- stt.py
- test_auth.py
- quota.py
- match_model.py
- v1/comm.py
- v1/auth.py
- safe_grooming_eval.py
- 채팅 읽음 상태 설계
- ThisAbled API 명세 요약 (v2.2)
- MATCH-02 추천 입력
- test_oauth_real.py
- config.py
- ThisAbled — Backend
- ThisAbled 기능 명세서 v2.2
- try_consume
- services/comm.py
- Q: 친구 추천 부분도 로딩이 안되는 문제가 있다고 하는데 확인 부탁함
- Q: 피그마 기준으로 게시물 카테고리 포함해서 누락된 백엔드 영역 기능 사항들 점검해줘
- Global Constraints
- SAFE 그루밍 평가 설계
- 14. 발달장애인 모드 및 AI 소통 코치
- 7. 피드·게시물·댓글
- conftest.py
- 11. AI 안심 채팅
- 1. 서비스 개요
- _BorrowedSession
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
- test_schema.py
- SAFE 그루밍 평가 결과
- test_media.py
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
- test_config.py
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
- safety_model.py
- Chat Read Status Implementation Plan
- Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?
- Q: 백엔드 핵심 소스코드 2개와 설명
- media_probe.py

## God Nodes (most connected - your core abstractions)
1. `User` - 82 edges
2. `register()` - 79 edges
3. `auth_header()` - 76 edges
4. `_Redis` - 37 edges
5. `_post()` - 33 edges
6. `Base` - 29 edges
7. `ChatMessage` - 28 edges
8. `send_media()` - 26 edges
9. `UiMode` - 24 edges
10. `PostCategory` - 23 edges

## Surprising Connections (you probably didn't know these)
- `test_withdraw_anonymize_keeps_posts_and_chat()` --indirect_call--> `ChatMessage`  [INFERRED]
  tests/test_withdrawal.py → app/models/chat.py
- `test_cleanup_deletes_stale_drafts()` --indirect_call--> `Post`  [INFERRED]
  tests/test_media.py → app/models/post.py
- `test_withdraw_anonymize_keeps_posts_and_chat()` --indirect_call--> `Post`  [INFERRED]
  tests/test_withdrawal.py → app/models/post.py
- `test_withdraw_delete_removes_posts()` --indirect_call--> `Post`  [INFERRED]
  tests/test_withdrawal.py → app/models/post.py
- `test_exclusion_rules_enforced_by_backend()` --indirect_call--> `FriendRequest`  [INFERRED]
  tests/test_match.py → app/models/social.py

## Import Cycles
- None detected.

## Communities (118 total, 46 thin omitted)

### Community 0 - "scheduler.py"
Cohesion: 0.23
Nodes (11): get_redis_client(), get_caption_caller(), (media_path, content_type) -> [{start,end,text}] 세그먼트. 실구현: Whisper., APScheduler 크론 — 드래프트 청소·자막 작업 복구·SAFE 재분석., §18.3: 모델 복구 감지용 주기 재분석 (unanalyzed·pending 텍스트)., 재시작 등으로 유실된 processing 자막 작업을 Redis 잠금 아래 재실행한다., _reanalyze_job(), recover_processing_captions() (+3 more)

### Community 1 - "users.py"
Cohesion: 0.05
Nodes (82): do_run_migrations(), run_async_migrations(), run_migrations_online(), list_notifications(), mark_read(), NotificationListOut, NotificationOut, AsyncSession (+74 more)

### Community 2 - "User"
Cohesion: 0.07
Nodes (84): async_sessionmaker, AsyncSession, BackgroundTasks, UploadFile, 미디어 업로드 — 사진(≤3장) · 영상(드래프트+자막 시작) · VIS-03 음성 입력., VIS-03 음성 입력 — 결과는 입력란 삽입용. 자동 게시하지 않는다 (§20-4)., 사진 업로드 (post 미연결) — POST /posts 의 media_ids로 연결한다., 영상 첨부 = processing 내부 드래프트 생성 + 자막 생성 즉시 시작 (POST-01·CAPTION-01). FE 길이는 빠른 거부용… (+76 more)

### Community 3 - "_Redis"
Cohesion: 0.18
Nodes (17): _acquire_caption_lock(), caption_chat_message_job(), caption_post_media_job(), describe_chat_message_job(), describe_post_media_job(), file_path_from_url(), _notify_chat_caption(), _notify_post_caption() (+9 more)

### Community 5 - "friends.py"
Cohesion: 0.06
Nodes (77): BlockedOut, create_block(), list_blocks(), AsyncSession, BaseModel, delete, get, UUID (+69 more)

### Community 6 - "ai_media.py"
Cohesion: 0.18
Nodes (17): AiResultCache, 동일 미디어 해시 캐싱 (VISION-01·CAPTION-01 중복 호출 방지, 비용 방어)., _cache_get(), _cache_put(), describe_image(), generate_caption(), get_describe_caller(), get_text_transcriber() (+9 more)

### Community 7 - "register"
Cohesion: 0.05
Nodes (99): user_channel(), RuntimeError, auth_header(), mock OAuth 가입 헬퍼 → {access_token, user_id, ...}., register(), _describe_fake(), make_friends(), CHAT-01 친구 채팅 · CHAT-02 비친구 요청 · 미디어 제한 (§4.5). (+91 more)

### Community 8 - "stt.py"
Cohesion: 0.23
Nodes (11): _extract_audio_to_m4a(), _get_client(), AsyncOpenAI, Path, OpenAI Whisper STT 서비스 (F02_S05 음성 댓글 / 자막). 엔드포인트는 `stt.transcribe(...)` 를…, 오디오 바이트 → 한국어 전사 텍스트. (실제 Whisper 호출, VIS-03 음성 입력), 최대 200MB 영상을 STT 상한 안의 단일 채널 M4A 음성으로 정규화한다., 영상/오디오 → 자막 세그먼트 [{start, end, text}] (CAPTION-01). (+3 more)

### Community 9 - "test_auth.py"
Cohesion: 0.29
Nodes (11): ACC-01/02 — 소셜 OAuth 전용 인증 (mock 제공자)., _signup_token(), test_callback_new_user_redirects_with_signup_token(), test_refresh_rotates_access_token(), test_rejoin_blocked_within_30_days(), test_signup_duplicate_nickname(), test_signup_forbidden_nickname(), test_signup_minor_blocks_stranger_requests() (+3 more)

### Community 10 - "quota.py"
Cohesion: 0.16
Nodes (24): caption_global_key(), caption_key(), caption_refund_marker(), consume_caption(), consume_caption_retry_attempt(), _minute(), Redis TTL 카운터 — VISION-01·CAPTION-01 사용자·서비스 전체 호출 한도. 키는 날짜/분 단위로 자연…, 내부 재시도도 실제 STT 1회이므로 서비스 전체 상한에 추가 반영한다. (+16 more)

### Community 11 - "match_model.py"
Cohesion: 0.32
Nodes (7): Features, health(), BaseModel, get, match-model mock — SBERT+LightGBM 모델 서버가 오기 전 자리 지킴이. 계약: POST /score {me,…, score(), ScoreIn

### Community 12 - "v1/comm.py"
Cohesion: 0.08
Nodes (52): BaseModel, RestrictionReleaseOut, _coach(), complete(), hints(), HintsOut, _post_context(), PostIn (+44 more)

### Community 13 - "v1/auth.py"
Cohesion: 0.06
Nodes (48): authorize(), callback(), _frontend_redirect(), logout(), AsyncSession, get, UUID, ACC-01/02 — 소셜 OAuth 전용 인증. 흐름: authorize → 제공자 로그인 → callback → FRONTEND_URL로… (+40 more)

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
Cohesion: 0.13
Nodes (18): callback_params(), 콜백 302 리다이렉트(Location=FRONTEND_URL?…)의 쿼리 파라미터 → 단일값 dict., test_existing_user_callback_logs_in(), test_invalid_mock_code_redirects_with_error(), _google_transport(), _kakao_transport(), fixture, 실 제공자(카카오·구글) OAuth 경로 — 외부 API를 MockTransport로 대체해 검증. 실키 없이 코드 경로(파라미터 인코딩·토큰… (+10 more)

### Community 19 - "config.py"
Cohesion: 0.22
Nodes (7): get_redis(), FastAPI 의존성. 테스트에서 override 가능하도록 분리., generate_description(), _get_client(), AsyncOpenAI, GPT-4o Vision 이미지 해설 서비스 (F02_S04 시각장애 모드). 엔드포인트는…, 이미지 바이트 → 한국어 해설 텍스트. (실제 GPT-4o 호출)

### Community 20 - "ThisAbled — Backend"
Cohesion: 0.15
Nodes (12): DB 스키마 (v3), graphify, Ralph 루프 (선택), ThisAbled — Backend, 기술 스택, 데드라인, 링크, 명령어 (+4 more)

### Community 21 - "ThisAbled 기능 명세서 v2.2"
Cohesion: 0.20
Nodes (9): 15. 마이페이지·설정, 16. 알림, 20. 핵심 인수 조건, 21. MVP 이후 계획, 2. 핵심 기능명, 3.1 포함, 3.2 제외 및 후속 범위, 3. MVP 범위 (+1 more)

### Community 22 - "try_consume"
Cohesion: 0.29
Nodes (8): consume_vision(), 일 20회·분 5회 동시 검증 — 분 한도 초과 시 일 카운터 롤백., 카운터 1 증가. 한도 초과면 롤백 후 False., CAPTION-01: 자막 생성 실패(재시도 소진) 시 일일 횟수 차감 복원., refund(), try_consume(), test_refund_restores_slot(), test_try_consume_respects_limit()

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

### Community 30 - "conftest.py"
Cohesion: 0.26
Nodes (12): client(), db(), _force_oauth_mock(), AsyncClient, fixture, 테스트 공용 픽스처. 각 테스트는 단일 커넥션 위의 외부 트랜잭션에서 실행되고 끝나면 롤백된다. 앱 코드가 `await db.commit()`…, .env의 실키·OAUTH_MOCK=false는 배포용 — 테스트는 항상 mock 제공자로 결정론적으로 실행한다. 개별…, 테스트와 API 요청이 같은 세션을 사용해 중첩 savepoint 간 간섭을 막는다. (+4 more)

### Community 31 - "11. AI 안심 채팅"
Cohesion: 0.33
Nodes (6): 11. AI 안심 채팅, SAFE-01 분석 원칙과 전달 타이밍, SAFE-02 탐지 범위, SAFE-03 사용자 표시, SAFE-04 내부 위험 점수, SAFE-05 관계 단위 자동 전송 제한 (신설)

### Community 32 - "1. 서비스 개요"
Cohesion: 0.33
Nodes (6): 1.1 서비스명, 1.2 서비스 정의 (한 문장), 1.3 서비스 비전, 1.4 해결하려는 문제, 1.5 핵심 사용자 경험, 1. 서비스 개요

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
Cohesion: 0.07
Nodes (28): health(), HealthOut, BaseModel, get, lifespan(), FastAPI, _add_error_response(), _guide() (+20 more)

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
Nodes (89): accept_request(), _author(), create_room(), _get_my_room(), list_messages(), list_requests(), list_rooms(), _message_out() (+81 more)

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

### Community 55 - "test_schema.py"
Cohesion: 0.29
Nodes (3): 스키마 v3 baseline 정합 검증 (설계: docs/superpowers/specs/2026-07-05-v2_1-refactor-…, 탈퇴 익명화(§15): 게시물·댓글·채팅 발신자는 SET NULL 가능해야 한다., test_anonymizable_fks_nullable()

### Community 63 - "SAFE 그루밍 평가 결과"
Cohesion: 0.40
Nodes (4): SAFE 그루밍 평가 결과, 기존 3a holdout, 신규 합성셋 결과, 진단

### Community 66 - "test_media.py"
Cohesion: 0.16
Nodes (18): PostMedia, 게시물 미디어 (사진≤3·영상 1개는 앱 검증). VISION 설명·CAPTION 자막 부착., cleanup_stale_drafts(), CAPTION-01: 업로드 후 24시간 미게시 내부 드래프트를 영상·자막과 함께 삭제. 이미 성공한 자막 생성의 일일 횟수 차감은 복원하지…, CallCounter, fake_ai(), _fake_duration(), fixture (+10 more)

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

### Community 89 - "test_config.py"
Cohesion: 0.20
Nodes (9): Settings, BaseSettings, _conn(), 테스트 전용 DB만 허용한다. 명시값이 없으면 현재 DB명에 `_test`를 붙인다., _test_database_url(), v2.1 명세 고정값이 Settings에 반영되어 있는지 검증., docker compose env_file은 POSTGRES_PASSWORD/REDIS_PASSWORD도 컨테이너 프로세스에 노출한다. 이…, test_settings_ignores_compose_only_env_vars() (+1 more)

### Community 118 - "safety_model.py"
Cohesion: 0.33
Nodes (6): analyze(), AnalyzeIn, health(), BaseModel, get, safety-model mock — AI 팀원의 자체 파인튜닝 안전 모델 서버가 오기 전 자리 지킴이. 계약: POST /analyze…

### Community 122 - "Chat Read Status Implementation Plan"
Cohesion: 0.25
Nodes (7): Chat Read Status Implementation Plan, File Structure, Global Constraints, Plan Self-Review, Task 1: Write failing behavior tests, Task 2: Persist and calculate the cursor, Task 3: Expose, document, verify, and commit

### Community 127 - "Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 기능명세에 채팅 기능에 읽음/안읽음 표시 있나?, Source Nodes

### Community 128 - "Q: 백엔드 핵심 소스코드 2개와 설명"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: 백엔드 핵심 소스코드 2개와 설명, Source Nodes

### Community 131 - "media_probe.py"
Cohesion: 0.38
Nodes (6): get_video_probe(), InvalidVideo, probe_video_duration(), Exception, Path, 서버가 직접 영상 컨테이너와 재생 시간을 검증한다.

## Knowledge Gaps
- **198 isolated node(s):** `thisabled-backend`, `프로젝트`, `기술 스택`, `명령어`, `DB 스키마 (v3)` (+193 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **46 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `caption_chat_message_job()` (3× useful, score=2.439148404)
- `save_upload()` (2× useful, score=1.998227986)
- `caption_post_media_job()` (2× useful, score=1.998227986)
- `caption_key()` (2× useful, score=1.998227986)
- `cleanup_stale_drafts()` (2× useful, score=1.998227986)
- `transcribe_segments()` (2× useful, score=1.998227986)
- `recommendations()` (2× useful, score=1.997288058)
- `UiMode` (2× useful, score=1.997288058)
- `user_features()` (2× useful, score=1.997288058)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `users.py`, `friends.py`, `register`, `v1/chat.py`, `v1/comm.py`, `v1/auth.py`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `_Redis` connect `_Redis` to `scheduler.py`, `User`, `friends.py`, `ai_media.py`, `main.py`, `v1/chat.py`, `quota.py`, `v1/auth.py`, `config.py`, `try_consume`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `auth_header()` connect `register` to `scheduler.py`, `test_media.py`, `test_auth.py`, `test_oauth_real.py`, `conftest.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `User` (e.g. with `callback()` and `refresh()`) actually correct?**
  _`User` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thisabled-backend`, `프로젝트`, `기술 스택` to the rest of the system?**
  _198 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `users.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05154639175257732 - nodes in this community are weakly interconnected._
- **Should `User` be split into smaller, more focused modules?**
  _Cohesion score 0.07099080694586313 - nodes in this community are weakly interconnected._