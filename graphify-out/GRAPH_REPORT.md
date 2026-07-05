# Graph Report - thisabled-backend  (2026-07-05)

## Corpus Check
- 53 files · ~19,195 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 407 nodes · 667 edges · 50 communities (38 shown, 12 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 17 edges (avg confidence: 0.62)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2f35b1a2`
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
- [[_COMMUNITY_0. 문서 정보|0. 문서 정보]]

## God Nodes (most connected - your core abstractions)
1. `register()` - 31 edges
2. `auth_header()` - 24 edges
3. `User` - 23 edges
4. `ThisAbled 기능 명세서 v2.1` - 23 edges
5. `Global Constraints` - 18 edges
6. `signup()` - 13 edges
7. `Base` - 13 edges
8. `ThisAbled — Backend` - 12 edges
9. `get_current_user()` - 11 edges
10. `login()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `login()` --indirect_call--> `User`  [INFERRED]
  app/api/v1/auth.py → app/models/user.py
- `recovery()` --indirect_call--> `User`  [INFERRED]
  app/api/v1/auth.py → app/models/user.py
- `me()` --references--> `User`  [EXTRACTED]
  app/api/v1/auth.py → app/models/user.py
- `UploadResponse` --uses--> `User`  [INFERRED]
  app/api/v1/upload.py → app/models/user.py
- `UserModeHistory` --uses--> `Base`  [INFERRED]
  app/models/user.py → app/db/session.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Docker Compose 스택 서비스 구성** — docker_compose_app, docker_compose_db, docker_compose_redis [EXTRACTED 0.90]

## Communities (50 total, 12 thin omitted)

### Community 0 - "Auth Test Suite"
Cohesion: 0.08
Nodes (38): AsyncClient, auth_header(), client(), 테스트 공용 픽스처.  각 테스트는 단일 커넥션 위의 외부 트랜잭션에서 실행되고 끝나면 롤백된다. 앱 코드가 `await db.commit()`, 가입 헬퍼 → signup 응답 JSON 반환 (access_token, user_id, recovery_code)., register(), _test_redis_url(), test_login_needs_onboarding_flips() (+30 more)

### Community 1 - "Auth Endpoints & JWT Security"
Cohesion: 0.14
Nodes (31): check_nickname(), login(), logout(), me(), _nickname_forbidden(), _nickname_taken(), AsyncSession, recovery() (+23 more)

### Community 2 - "App Core, Upload & Config"
Cohesion: 0.08
Nodes (27): UploadFile, upload_image(), UploadResponse, describe_image(), Redis, /uploads/<name> → 로컬 파일 경로. 경로 탈출 방지(basename만 사용)., _resolve_upload_path(), Settings (+19 more)

### Community 3 - "Posts API & DB Models"
Cohesion: 0.16
Nodes (23): create_post(), delete_post(), get_post(), list_posts(), AsyncSession, UploadFile, transcribe(), get_current_user() (+15 more)

### Community 4 - "GPT-4o Vision + Redis Cache"
Cohesion: 0.13
Nodes (14): 0. 확정된 결정, 1. DB 스키마 v3 (baseline), 2. 아키텍처, 3. API 표면 (v1), 4. 문서 산출물, 5. 테스트 전략, 6. 구현 순서 (빅뱅), 7. 명세와의 정합 노트 (구현 설계에서 확정한 값) (+6 more)

### Community 5 - "Infra & Deployment Policy"
Cohesion: 0.50
Nodes (5): app 서비스 (FastAPI), db 서비스 (PostgreSQL 15), db/redis 호스트 포트 미노출 (내부 네트워크), app 루프백 바인딩 (127.0.0.1:8000), redis 서비스 (Redis 7)

### Community 6 - "User Disability-Mode Settings"
Cohesion: 0.27
Nodes (12): get_mode(), AsyncSession, update_mode(), DisabilityMode, 모드 + 사용자별 미세조정(overrides)을 합친 최종 설정., settings_for(), 모드 변경 이력 (F02_S08, 베타테스트 분석용)., UserModeHistory (+4 more)

### Community 8 - "Whisper STT Service"
Cohesion: 0.10
Nodes (20): Global Constraints, Task 10: friends & blocks, Task 11: chat REST + SAFE 동기 파이프라인 + SAFE-05, Task 12: WebSocket + Redis pub/sub, Task 13: notifications, Task 14: recommendations + comm (모델 서버·LLM stub 경계), Task 15: mock 모델 서버 2종 + compose 배선, Task 16: 정리·전체 그린·문서 최종 정합 (+12 more)

### Community 9 - "get_redis"
Cohesion: 0.07
Nodes (27): 0. 사전 점검, 1) refresh 쿠키 SameSite — 이미 반영됨 ✅, 1. Tailscale 설치 & 로그인, 2) `.env` 설정, 2. Funnel 기능 켜기 (최초 1회, 콘솔에서), 3. Funnel 실행, 3) 프론트 fetch, Cloudflare Tunnel과 비교 (+19 more)

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
Nodes (9): 15. 마이페이지·설정, 16. 알림, 20. 핵심 인수 조건, 21. MVP 이후 계획, 2. 핵심 기능명, 5.1 주요 화면, 5.2 UI 모드 전환, 5. 공통 화면 구조 (+1 more)

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
Cohesion: 0.60
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

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
Cohesion: 0.67
Nodes (3): 3.1 포함, 3.2 제외 및 후속 범위, 3. MVP 범위

### Community 39 - "5. 공통 화면 구조"
Cohesion: 0.40
Nodes (5): _get_client(), AsyncOpenAI, OpenAI Whisper STT 서비스 (F02_S05 음성 댓글 / 자막).  엔드포인트는 `stt.transcribe(...)` 를 호출한, 오디오 바이트 → 한국어 전사 텍스트. (실제 Whisper 호출), transcribe()

### Community 49 - "0. 문서 정보"
Cohesion: 0.67
Nodes (3): 0.1 v2.1 주요 개정 사항, 0.2 v2.0 주요 개정 사항 (이력), 0. 문서 정보

## Knowledge Gaps
- **154 isolated node(s):** `thisabled-backend`, `프로젝트`, `기술 스택`, `명령어`, `DB 스키마 (v3)` (+149 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ThisAbled 기능 명세서 v2.1` connect `ThisAbled 기능 명세서 v2.1` to `6. 회원가입 및 계정`, `10. 1:1 채팅`, `13. 청각장애인 모드`, `18. 기술 구성`, `19. 비기능 요구사항`, `9. 친구·차단`, `3. MVP 범위`, `0. 문서 정보`, `MATCH-02 추천 입력`, `14. 발달장애인 모드 및 AI 소통 코치`, `7. 피드·게시물·댓글`, `11. AI 안심 채팅`, `1. 서비스 개요`, `4. 사용자 정책`, `12. 시각장애인 모드`, `17. 외부 AI 사용 및 데이터 처리 원칙`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `User` connect `Posts API & DB Models` to `Auth Endpoints & JWT Security`, `App Core, Upload & Config`, `User Disability-Mode Settings`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `User` (e.g. with `login()` and `recovery()`) actually correct?**
  _`User` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `thisabled-backend`, `v2.1 명세 고정값이 Settings에 반영되어 있는지 검증.`, `/uploads/<name> → 로컬 파일 경로. 경로 탈출 방지(basename만 사용).` to the rest of the system?**
  _176 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Auth Test Suite` be split into smaller, more focused modules?**
  _Cohesion score 0.07518796992481203 - nodes in this community are weakly interconnected._
- **Should `Auth Endpoints & JWT Security` be split into smaller, more focused modules?**
  _Cohesion score 0.14264264264264265 - nodes in this community are weakly interconnected._
- **Should `App Core, Upload & Config` be split into smaller, more focused modules?**
  _Cohesion score 0.08205128205128205 - nodes in this community are weakly interconnected._