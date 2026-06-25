# Ralph 루프 태스크

자율 반복 개발 루프(Ralph Wiggum 기법). `ralph-loop` 플러그인이 Stop hook으로
세션 종료를 가로채 같은 프롬프트를 반복 투입하고, 완료 약속어가 나오면 멈춘다.

## 실행 방법

태스크 파일(`docs/ralph/<task>.md`)을 작성한 뒤:

```
/ralph-loop "docs/ralph/<task>.md 의 태스크를 구현하라.
각 반복마다: 태스크 1개 완전 구현 → pytest 통과 → 1커밋.
모든 항목이 끝나고 pytest가 그린이면 <promise>RALPH_DONE</promise> 출력."
--completion-promise "RALPH_DONE" --max-iterations 10
```

## 안전장치 (필수)

- **`--max-iterations`는 반드시 지정** (기본 무제한 = 비용 폭주 위험). 보통 5~10.
- **테스트가 완료 판정 기준**: `docker compose exec -T app pytest -q` 그린이어야 약속어 출력.
- 루프 상태는 `.claude/ralph-loop.local.md`(gitignore). `/cancel-ralph`로 중단.

## 태스크 파일 작성 규칙

- 한 파일 = 한 기능 단위(F0X 또는 그 하위). 범위를 좁게.
- **명세 출처를 명시**(Notion F0X 링크/요지). 코드가 명세를 앞서가지 않도록.
- **완료 조건(Definition of Done)을 체크리스트로** 명확히. Ralph가 이걸로 자기 진척을 판단.
- 각 항목은 "구현 + 대응 테스트"를 한 세트로.

## 워크플로우 정합

- 1 태스크 = 1 커밋 (CLAUDE.md 커밋 규칙과 동일)
- 큰 기능은 worktree에서 Ralph 실행 → `finishing-a-development-branch`로 통합
- 착수 전 모호하면 `brainstorming`으로 스펙부터 확정 (CLAUDE.md 명세 검증 게이트)

예시: [example-task.md](example-task.md)
