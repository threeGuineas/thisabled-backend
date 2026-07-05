# ThisAbled — Backend

## 프로젝트
2026 한이음 드림업 / 장애 유형별 적응형 UI 소셜 플랫폼. 팀: FE 1 + BE 1(나) + AI 1.
모드: 시각(GPT-4o Vision 해설 + Whisper 댓글) · 발달(KoBERT 그루밍·혐오 탐지) · 청각(자막 + 소통 코칭, 중간평가 후).

## 기술 스택
Python 3.11 · FastAPI · PostgreSQL 15 · Redis 7 · Docker Compose · JWT(python-jose) · Alembic.
AI 연동(GPT-4o Vision, Whisper)·WebSocket 채팅은 S2 이후.
> GPT-4o 호출은 Redis 캐싱 필수(동일 이미지 중복 호출 방지, 월 예산 30만원).

## 명령어
```bash
docker compose up -d                                     # 전체 환경 실행
docker compose exec -T app pytest -q                     # 전체 테스트
docker compose exec -T app pytest tests/test_auth.py -q  # 파일 단위
```
main은 항상 `pytest` 그린 유지.

## DB 스키마
- **PK·FK 전부 UUID.** 정본은 마이그레이션: `alembic/versions/*_schema_v2_auth_mode.py`
- 테이블: `users`, `forbidden_nicknames`, `user_mode_history`, `posts`, `messages`, `reports`
- `disability_mode`: `visual` | `hearing` | `developmental` | `default` (NULL = 온보딩 미완료)
- ⚠️ `reports`는 F03 명세상 message 단위 재설계 예정(M1). `messages` 안전감시 컬럼도 M1.
- ERD 산출물: `docs/erd.dbml`

## 워크플로우
- **feature 브랜치 모델**: `git switch -c feature/<이름>` 분기 → 완료 시 `finishing-a-development-branch` 스킬로 테스트 통과 검증 → PR → main 병합 → 브랜치 삭제. 문서·설정 같은 작은 단일 작업만 main 직접.
- ⚠️ **워크트리 금지**: compose 포트(8000/5432/6379) 고정이라 병렬 스택이 충돌. 필요하면 포트 변수화 선행.
- **1 논리 변경 = 1 커밋**, 테스트 통과 후에만 커밋. 신규 엔드포인트·스키마 변경은 대응 테스트를 같은 커밋에.

## 명세 검증 (코드로 옮기기 전)
새 기능·엔드포인트·스키마는 착수 전 `brainstorming` 스킬로 의도·설계를 먼저 끌어내고, Notion F0X 명세를 읽어 모호함을 제거한다. 코드부터 뛰어들지 않는다.
명세 읽을 때 의심할 것: 수치 정합(SP 합·토큰 만료·길이) / 단정문 속 [TBD] / ID 체계 중복 / 라이브러리 혼동(PostGIS vs pgvector) / 문서 간 동기화 / 시점 모순 / 코드–명세 드리프트.
발견한 결함은 **코드에서 임의 우회 금지** — Notion 명세를 고치거나 팀 안건으로 올린다.

## Ralph 루프 (선택)
잘 정의된 단일 기능의 구현→테스트→커밋 자율 반복. `ralph-loop` 플러그인 활성.
```
/ralph-loop "<프롬프트>" --completion-promise "RALPH_DONE" --max-iterations 10
```
`--max-iterations` 필수(미지정 = 비용 폭주, 보통 5~10). 완료 판정 = pytest 그린. 1 태스크 = 1 커밋. 중단 `/cancel-ralph`.

## 커밋 메시지
Conventional Commits: `<type>(<scope>): <subject>`
- type: `feat` `fix` `chore` `refactor` `docs` `test` `ci`
- scope: `auth` `posts` `users` `messages` `reports` `db` `infra` `ai`
- subject 명령형 50자 이내(한글 가능). 스프린트 커밋은 끝에 현재 스프린트 태그(예: `[S2]`).
- 본문 필요 시 빈 줄 후 `Why:` / `How:` 로 맥락 기록.

## 데드라인
`7/14` ⚠️ 중간평가 마감 (영상 + 보고서 + SW 설계서 7종 / 백엔드 담당: 핵심 소스코드 발췌)
`10/30` 🎯 최종 제출

## 링크
노션 프로젝트: https://app.notion.com/p/2026-89bcd5876410821fa56c010112bf543c

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
