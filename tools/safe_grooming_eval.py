"""Evaluate a SAFE model server against grooming-focused JSONL cases."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REQUIRED_FIELDS = {
    "case_id",
    "text",
    "expected_risk",
    "subcategory",
    "receiver_is_minor",
    "notes",
}
VALID_VERDICTS = {"safe", "flagged"}


def validate_case(case: dict[str, Any]) -> None:
    missing = REQUIRED_FIELDS - case.keys()
    if missing:
        raise ValueError(f"missing required fields: {', '.join(sorted(missing))}")
    if not isinstance(case["case_id"], str) or not case["case_id"].strip():
        raise ValueError("case_id must be a non-empty string")
    if not isinstance(case["text"], str) or not case["text"].strip():
        raise ValueError("text must be a non-empty string")
    if not isinstance(case["expected_risk"], bool):
        raise ValueError("expected_risk must be boolean")
    if not isinstance(case["subcategory"], str) or not case["subcategory"].strip():
        raise ValueError("subcategory must be a non-empty string")
    if not isinstance(case["receiver_is_minor"], bool):
        raise ValueError("receiver_is_minor must be boolean")
    if not isinstance(case["notes"], str):
        raise ValueError("notes must be a string")


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                case = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
            if not isinstance(case, dict):
                raise ValueError(f"{path}:{line_number}: case must be an object")
            try:
                validate_case(case)
            except ValueError as exc:
                raise ValueError(f"{path}:{line_number}: {exc}") from exc
            cases.append(case)
    if not cases:
        raise ValueError(f"{path}: no cases found")
    return cases


def _rate(numerator: int, denominator: int) -> float | None:
    return round(numerator / denominator, 4) if denominator else None


def _group_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [row for row in rows if not row.get("error") and row.get("verdict") in VALID_VERDICTS]
    positives = [row for row in valid if row["expected_risk"]]
    boundaries = [row for row in valid if not row["expected_risk"]]
    true_positive = sum(row["verdict"] == "flagged" for row in positives)
    false_positive = sum(row["verdict"] == "flagged" for row in boundaries)
    return {
        "support": len(valid),
        "flagged": sum(row["verdict"] == "flagged" for row in valid),
        "positive_support": len(positives),
        "recall": _rate(true_positive, len(positives)),
        "fnr": _rate(len(positives) - true_positive, len(positives)),
        "boundary_support": len(boundaries),
        "fpr": _rate(false_positive, len(boundaries)),
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [row for row in results if not row.get("error") and row.get("verdict") in VALID_VERDICTS]
    errors = len(results) - len(valid)
    report: dict[str, Any] = {
        "counts": {"total": len(results), "valid": len(valid), "errors": errors},
        "overall": _group_metrics(results),
        "by_subcategory": {},
        "by_receiver": {},
    }
    subcategories = sorted({row["subcategory"] for row in results})
    for subcategory in subcategories:
        report["by_subcategory"][subcategory] = _group_metrics(
            [row for row in results if row["subcategory"] == subcategory]
        )
    for key, is_minor in (("minor", True), ("adult", False)):
        report["by_receiver"][key] = _group_metrics(
            [row for row in results if row["receiver_is_minor"] is is_minor]
        )
    return report


def _post_analyze(base_url: str, case: dict[str, Any], timeout: float) -> dict[str, Any]:
    payload = json.dumps(
        {"text": case["text"], "receiver_is_minor": case["receiver_is_minor"]},
        ensure_ascii=False,
    ).encode("utf-8")
    request = Request(
        f"{base_url.rstrip('/')}/analyze",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    verdict = body.get("verdict") if isinstance(body, dict) else None
    if verdict not in VALID_VERDICTS:
        raise ValueError(f"invalid verdict: {verdict!r}")
    return body


def evaluate(base_url: str, cases: list[dict[str, Any]], timeout: float = 10.0) -> list[dict[str, Any]]:
    results = []
    for case in cases:
        result = {key: case[key] for key in ("case_id", "expected_risk", "subcategory", "receiver_is_minor")}
        try:
            body = _post_analyze(base_url, case, timeout)
            result["verdict"] = body["verdict"]
            result["response"] = body
        except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            result["verdict"] = None
            result["error"] = f"{type(exc).__name__}: {exc}"
        results.append(result)
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="SAFE model base URL, e.g. http://localhost:9001")
    parser.add_argument("--input", type=Path, required=True, help="Input JSONL case file")
    parser.add_argument("--output", type=Path, required=True, help="Output JSON report")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args(argv)

    cases = load_cases(args.input)
    results = evaluate(args.url, cases, timeout=args.timeout)
    summary = summarize(results)
    report = {
        "evaluation": "safe_grooming_synthetic_v1",
        "input": str(args.input),
        "server": args.url,
        "limitations": [
            "synthetic evaluation only; it does not replace real-data validation",
            "single-message cases cannot measure multi-turn grooming context",
        ],
        "summary": summary,
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 2 if summary["counts"]["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
