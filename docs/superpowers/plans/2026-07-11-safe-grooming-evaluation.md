# SAFE Grooming Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reproducible, server-contract-compatible synthetic evaluation for SAFE grooming misses, including staged signals and false-positive boundary cases.

**Architecture:** Keep the evaluation self-contained in the backend workspace. A JSONL fixture defines labeled cases, a small pure metrics module computes recall/FNR/FPR and subgroup summaries, and a CLI runner sends cases to the existing SAFE `/analyze` endpoint and writes raw plus aggregate JSON. No model or backend production behavior changes.

**Tech Stack:** Python 3.11, standard library `json`/`argparse`/`urllib` or existing HTTP client, pytest, JSONL.

## Global Constraints

- SAFE model contract is `POST /analyze {text, receiver_is_minor} -> {verdict: safe|flagged}`.
- Model verdict is the only correctness field; diagnostic response fields are optional.
- Synthetic results must be reported separately from real-data results.
- Do not modify the sibling `thisabled-ai` repository or its existing dirty changes.
- Do not change production SAFE, chat, schema, or model-serving code.
- Use the existing backend workspace branch; do not create a worktree because compose ports are fixed.

---

### Task 1: Add the evaluation fixture and pure metric tests

**Files:**
- Create: `tests/fixtures/safe_grooming_cases.jsonl`
- Create: `tests/test_safe_grooming_eval.py`
- Create: `tools/safe_grooming_eval.py`

**Interfaces:**
- Tests will consume `load_cases(path)`, `summarize(results)`, and `validate_case(case)` from `tools.safe_grooming_eval`.
- A case has `case_id`, `text`, `expected_risk`, `subcategory`, `receiver_is_minor`, and `notes`.

- [ ] **Step 1: Write the failing tests**

  Add tests that assert:
  - the fixture contains both positive and boundary cases;
  - every fixture row passes schema validation;
  - a synthetic result set yields overall recall, FNR, boundary FPR, and per-subcategory counts;
  - an invalid verdict is counted as an error rather than as `safe`.

- [ ] **Step 2: Run tests to verify the expected failure**

  Run: `pytest -q tests/test_safe_grooming_eval.py`

  Expected: collection fails because `tools.safe_grooming_eval` does not yet exist.

- [ ] **Step 3: Create the fixture**

  Add 26 detection cases across `intimacy`, `isolation`, `dependency`, `secrecy_boundary`, `combined`, and `minimal_signal`, plus 12 boundary cases across `mutual_friendship`, `professional_help`, and `ordinary_encouragement`. Keep at least 30% of positive cases in a disability-support context and include adult/minor receiver variants.

### Task 2: Implement the pure evaluator and CLI

**Files:**
- Create: `tools/__init__.py`
- Create: `tools/safe_grooming_eval.py`

**Interfaces:**
- `load_cases(path: Path) -> list[dict]`
- `validate_case(case: dict) -> None`
- `summarize(results: list[dict]) -> dict`
- `evaluate(base_url: str, cases: list[dict], timeout: float) -> list[dict]`
- CLI: `python -m tools.safe_grooming_eval --url http://localhost:9001 --input tests/fixtures/safe_grooming_cases.jsonl --output /tmp/safe-grooming-eval.json`

- [ ] **Step 1: Implement only enough to satisfy the tests**

  Validate required fields and value domains, compute counts using `expected_risk`/`verdict`, and preserve request errors in result rows. Do not silently convert missing or invalid verdicts to `safe`.

- [ ] **Step 2: Run the focused tests**

  Run: `pytest -q tests/test_safe_grooming_eval.py`

  Expected: all focused tests pass.

- [ ] **Step 3: Run a no-server smoke command**

  Run the CLI against an unused local port and verify it writes an error-bearing report without reporting a false model score.

### Task 3: Run the real SAFE evaluation

**Files:**
- Create: `reports/safe-grooming-eval-2026-07-11.json`

- [ ] **Step 1: Start only the existing SAFE model service**

  Run: `docker compose up -d safety-model`

- [ ] **Step 2: Wait for `/health` and run the evaluator**

  Run: `python -m tools.safe_grooming_eval --url http://localhost:9001 --input tests/fixtures/safe_grooming_cases.jsonl --output reports/safe-grooming-eval-2026-07-11.json`

- [ ] **Step 3: Compare with the existing AI repository 3a holdout**

  If the service is available, run the same evaluator against a normalized copy of `../thisabled-ai/data/synthetic/emergency/3a/test.jsonl` without modifying that repository. Report the new staged cases separately from the existing 50-case holdout.

### Task 4: Verify and document limitations

**Files:**
- Modify: `docs/superpowers/specs/2026-07-11-safe-grooming-evaluation-design.md`
- Modify: `reports/safe-grooming-eval-2026-07-11.json`

- [ ] **Step 1: Run verification**

  Run: `pytest -q tests/test_safe_grooming_eval.py`

  Run: `python -m tools.safe_grooming_eval --help`

- [ ] **Step 2: Check output requirements**

  Confirm the report includes overall recall/FNR, boundary FPR, subgroup metrics, invalid/error count, and the synthetic/single-turn limitation.

- [ ] **Step 3: Run `graphify update .`**

  Update the code graph after modifications.

- [ ] **Step 4: Commit the evaluation artifacts**

  Run: `git add docs/superpowers/specs/2026-07-11-safe-grooming-evaluation-design.md docs/superpowers/plans/2026-07-11-safe-grooming-evaluation.md tools tests/fixtures reports/safe-grooming-eval-2026-07-11.json`

  Run: `git commit -m "test(safe): evaluate grooming detection cases"`
