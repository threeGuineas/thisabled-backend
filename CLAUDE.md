# ThisAbled — Backend

## 프로젝트
2026 한이음 드림업 / 장애 유형별 적응형 UI 소셜 플랫폼. 팀: FE 1 + BE 1(나) + AI 1.
기능 축(명세 v2.1): MODE(시각·청각·발달 UI) · SAFE(채팅 텍스트 위험 감지, 자체 모델) · COMM(LLM 소통 코치) · MATCH(SBERT+LightGBM 친구 추천) · CAPTION(Whisper 자막) · VISION(사진 설명).

## 기술 스택
Python 3.11 · FastAPI · PostgreSQL 15 · Redis 7 · Docker Compose · Alembic · WebSocket(+Redis pub/sub).
인증: 소셜 로그인 OAuth 전용(카카오·구글, dev는 **mock 제공자** — 실키는 환경변수 교체) + JWT(python-jose).
SAFE·MATCH 모델은 **별도 모델 서버 HTTP 경계**(AI 팀원 담당, 현재 compose mock). COMM·CAPTION·VISION은 외부 AI API(서버 경유).
> 외부 AI 호출은 미디어 해시 캐싱(ai_result_cache) + 사용자별 한도(Redis) 필수 — vision 20/일·5/분, caption 5/일, 월 예산 30만원.

## 명령어
```bash
docker compose up -d                                     # 전체 환경 실행
docker compose exec -T app pytest -q                     # 전체 테스트
docker compose exec -T app pytest tests/test_auth.py -q  # 파일 단위
```
main은 항상 `pytest` 그린 유지.

## DB 스키마 (v3)
- **PK·FK 전부 UUID.** 정본은 v3 baseline 마이그레이션: `alembic/versions/*_schema_v3_baseline.py` (v2 체인 폐기, drop & recreate)
- 테이블: `users` `social_identities` `withdrawn_socials` `interest_tags` `user_interest_tags` `forbidden_nicknames` `user_mode_history` `posts` `post_media` `comments` `post_likes` `friend_requests` `friendships` `blocks` `chat_rooms` `chat_messages` `send_restrictions` `notifications` `ai_result_cache`
- `ui_mode`: `visual` | `hearing` | `developmental` (v2.1에 'default' 없음, 가입 완료 시 필수)
- 신고(reports)는 MVP 제외(명세 §3.2) — 테이블·코드 없음. 만 나이·연령대는 저장하지 않고 `birth_date`로 매번 계산.
- ERD 산출물: `docs/erd.dbml` / 설계 근거: `docs/superpowers/specs/2026-07-05-v2_1-refactor-design.md`

## 워크플로우
- **feature 브랜치 모델**: `git switch -c feature/<이름>` 분기 → 완료 시 `finishing-a-development-branch` 스킬로 테스트 통과 검증 → PR → main 병합 → 브랜치 삭제. 문서·설정 같은 작은 단일 작업만 main 직접.
- ⚠️ **워크트리 금지**: compose 포트(8000/5432/6379) 고정이라 병렬 스택이 충돌. 필요하면 포트 변수화 선행.
- **1 논리 변경 = 1 커밋**, 테스트 통과 후에만 커밋. 신규 엔드포인트·스키마 변경은 대응 테스트를 같은 커밋에.

## 명세 검증 (코드로 옮기기 전)
**SSOT는 `docs/ThisAbled_기능명세서_v2_1.md`** (식별자: ACC/TAG/FEED/POST/VISION/CAPTION/MATCH/FRIEND/BLOCK/CHAT/SAFE/COMM). 새 기능·엔드포인트·스키마는 착수 전 `brainstorming` 스킬로 의도·설계를 먼저 끌어내고, 해당 식별자 절을 읽어 모호함을 제거한다. 코드부터 뛰어들지 않는다.
명세 읽을 때 의심할 것: 수치 정합(한도·기간·길이) / 단정문 속 [TBD] / 식별자 중복 / 문서 간 동기화 / 시점 모순 / 코드–명세 드리프트.
발견한 결함은 **코드에서 임의 우회 금지** — 명세서를 고치거나 팀 안건으로 올린다.

## Ralph 루프 (선택)
잘 정의된 단일 기능의 구현→테스트→커밋 자율 반복. `ralph-loop` 플러그인 활성.
```
/ralph-loop "<프롬프트>" --completion-promise "RALPH_DONE" --max-iterations 10
```
`--max-iterations` 필수(미지정 = 비용 폭주, 보통 5~10). 완료 판정 = pytest 그린. 1 태스크 = 1 커밋. 중단 `/cancel-ralph`.

## 커밋 메시지
Conventional Commits: `<type>(<scope>): <subject>`
- type: `feat` `fix` `chore` `refactor` `docs` `test` `ci`
- scope: `auth` `users` `posts` `friends` `chat` `safe` `comm` `match` `db` `infra` `ai`
- subject 명령형 50자 이내(한글 가능). 스프린트 커밋은 끝에 현재 스프린트 태그(예: `[S2]`).
- 본문 필요 시 빈 줄 후 `Why:` / `How:` 로 맥락 기록.

## 데드라인
`7/14` ⚠️ 중간평가 마감 (영상 + 보고서 + SW 설계서 7종 / 백엔드 담당: 핵심 소스코드 발췌)
`10/30` 🎯 최종 제출

## 링크
- 기능명세서(SSOT): `docs/ThisAbled_기능명세서_v2_1.md`
- 노션 프로젝트: https://app.notion.com/p/2026-89bcd5876410821fa56c010112bf543c

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
