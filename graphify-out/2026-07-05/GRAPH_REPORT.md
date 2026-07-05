# Graph Report - .  (2026-07-04)

## Corpus Check
- Corpus is ~7,333 words - fits in a single context window. You may not need a graph.

## Summary
- 228 nodes · 505 edges · 21 communities (18 shown, 3 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 23 edges (avg confidence: 0.68)
- Token cost: 41,000 input · 2,568 output

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
- [[_COMMUNITY_Alembic Migration Runner|Alembic Migration Runner]]
- [[_COMMUNITY_Project Concept|Project Concept]]
- [[_COMMUNITY_Feature Branch Workflow|Feature Branch Workflow]]
- [[_COMMUNITY_Repository Root|Repository Root]]

## God Nodes (most connected - your core abstractions)
1. `register()` - 31 edges
2. `auth_header()` - 24 edges
3. `User` - 23 edges
4. `signup()` - 13 edges
5. `Base` - 13 edges
6. `get_current_user()` - 11 edges
7. `login()` - 9 edges
8. `Post` - 8 edges
9. `update_mode()` - 7 edges
10. `create_access_token()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `워크트리 금지 (포트 고정 충돌)` --rationale_for--> `app 서비스 (FastAPI)`  [INFERRED]
  CLAUDE.md → docker-compose.yml
- `GPT-4o 호출 Redis 캐싱 정책` --conceptually_related_to--> `redis 서비스 (Redis 7)`  [INFERRED]
  CLAUDE.md → docker-compose.yml
- `OpenAI 비용 노출 위험 (vision/stt)` --conceptually_related_to--> `GPT-4o 호출 Redis 캐싱 정책`  [INFERRED]
  docs/deploy-tunnel.md → CLAUDE.md
- `DB 스키마 (users/posts/messages/reports 등)` --shares_data_with--> `db 서비스 (PostgreSQL 15)`  [INFERRED]
  CLAUDE.md → docker-compose.yml
- `Ralph 루프 태스크 가이드` --references--> `명세 검증 게이트`  [EXTRACTED]
  docs/ralph/README.md → CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **터널 노출 시 크로스오리진 대응 3종 세트** — docs_deploy_tunnel_refresh_cookie_samesite, docs_deploy_tunnel_cors_origins, docs_deploy_tunnel_guide [EXTRACTED 0.90]
- **Docker Compose 스택 서비스 구성** — docker_compose_app, docker_compose_db, docker_compose_redis [EXTRACTED 0.90]

## Communities (21 total, 3 thin omitted)

### Community 0 - "Auth Test Suite"
Cohesion: 0.08
Nodes (38): AsyncClient, auth_header(), client(), 테스트 공용 픽스처.  각 테스트는 단일 커넥션 위의 외부 트랜잭션에서 실행되고 끝나면 롤백된다. 앱 코드가 `await db.commit()`, 가입 헬퍼 → signup 응답 JSON 반환 (access_token, user_id, recovery_code)., register(), _test_redis_url(), test_login_needs_onboarding_flips() (+30 more)

### Community 1 - "Auth Endpoints & JWT Security"
Cohesion: 0.15
Nodes (30): check_nickname(), login(), logout(), _nickname_forbidden(), _nickname_taken(), AsyncSession, recovery(), refresh() (+22 more)

### Community 2 - "App Core, Upload & Config"
Cohesion: 0.13
Nodes (19): me(), UploadFile, transcribe(), UploadFile, upload_image(), UploadResponse, Settings, get_current_user() (+11 more)

### Community 3 - "Posts API & DB Models"
Cohesion: 0.19
Nodes (18): create_post(), delete_post(), get_post(), list_posts(), AsyncSession, Base, get_db(), Message (+10 more)

### Community 4 - "GPT-4o Vision + Redis Cache"
Cohesion: 0.16
Nodes (15): describe_image(), Redis, /uploads/<name> → 로컬 파일 경로. 경로 탈출 방지(basename만 사용)., _resolve_upload_path(), get_redis(), get_redis_client(), Redis, FastAPI 의존성. 테스트에서 override 가능하도록 분리. (+7 more)

### Community 5 - "Infra & Deployment Policy"
Cohesion: 0.16
Nodes (15): DB 스키마 (users/posts/messages/reports 등), GPT-4o 호출 Redis 캐싱 정책, PK·FK 전부 UUID 정책, 워크트리 금지 (포트 고정 충돌), app 서비스 (FastAPI), db 서비스 (PostgreSQL 15), db/redis 호스트 포트 미노출 (내부 네트워크), app 루프백 바인딩 (127.0.0.1:8000) (+7 more)

### Community 6 - "User Disability-Mode Settings"
Cohesion: 0.32
Nodes (10): get_mode(), AsyncSession, update_mode(), DisabilityMode, 모드 + 사용자별 미세조정(overrides)을 합친 최종 설정., settings_for(), ModeResponse, ModeUpdateRequest (+2 more)

### Community 7 - "Dev Workflow & Ralph Loop"
Cohesion: 0.29
Nodes (8): Conventional Commits 규칙, Ralph 루프 (자율 반복 개발), 명세 검증 게이트, Definition of Done 체크리스트, 예시 태스크: 게시글 수정 API (PUT /posts/{id}), Ralph 루프 태스크 가이드, --max-iterations 필수 안전장치, pytest 그린 = 완료 판정 기준

### Community 8 - "Whisper STT Service"
Cohesion: 0.40
Nodes (5): _get_client(), AsyncOpenAI, OpenAI Whisper STT 서비스 (F02_S05 음성 댓글 / 자막).  엔드포인트는 `stt.transcribe(...)` 를 호출한, 오디오 바이트 → 한국어 전사 텍스트. (실제 Whisper 호출), transcribe()

### Community 9 - "Alembic Migration Runner"
Cohesion: 0.60
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

## Knowledge Gaps
- **8 isolated node(s):** `thisabled-backend`, `ThisAbled 백엔드 프로젝트`, `장애 유형별 적응형 UI 모드`, `feature 브랜치 워크플로우`, `명세 검증 게이트` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `App Core, Upload & Config` to `Auth Endpoints & JWT Security`, `Posts API & DB Models`, `GPT-4o Vision + Redis Cache`, `User Disability-Mode Settings`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `User` (e.g. with `login()` and `recovery()`) actually correct?**
  _`User` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `/uploads/<name> → 로컬 파일 경로. 경로 탈출 방지(basename만 사용).`, `모드 + 사용자별 미세조정(overrides)을 합친 최종 설정.`, `F01_S08: 가입 시 1회 노출하는 12자리 복구 코드.` to the rest of the system?**
  _30 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Auth Test Suite` be split into smaller, more focused modules?**
  _Cohesion score 0.07518796992481203 - nodes in this community are weakly interconnected._
- **Should `Auth Endpoints & JWT Security` be split into smaller, more focused modules?**
  _Cohesion score 0.1492063492063492 - nodes in this community are weakly interconnected._
- **Should `App Core, Upload & Config` be split into smaller, more focused modules?**
  _Cohesion score 0.12698412698412698 - nodes in this community are weakly interconnected._