import json
from pathlib import Path

import pytest

from tools.safe_grooming_eval import load_cases, summarize, validate_case


FIXTURE = Path(__file__).parent / "fixtures" / "safe_grooming_cases.jsonl"


def test_fixture_contains_detection_and_boundary_cases():
    cases = load_cases(FIXTURE)

    assert len(cases) == 38
    assert any(case["expected_risk"] for case in cases)
    assert any(not case["expected_risk"] for case in cases)
    assert sum(case["receiver_is_minor"] for case in cases) >= 6


def test_fixture_rows_match_case_schema():
    for line in FIXTURE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            validate_case(json.loads(line))


def test_summarize_reports_recall_fnr_fpr_and_subgroups():
    results = [
        {
            "case_id": "a",
            "expected_risk": True,
            "subcategory": "isolation",
            "receiver_is_minor": True,
            "verdict": "flagged",
        },
        {
            "case_id": "b",
            "expected_risk": True,
            "subcategory": "dependency",
            "receiver_is_minor": False,
            "verdict": "safe",
        },
        {
            "case_id": "c",
            "expected_risk": False,
            "subcategory": "professional_help",
            "receiver_is_minor": True,
            "verdict": "flagged",
        },
        {
            "case_id": "d",
            "expected_risk": False,
            "subcategory": "mutual_friendship",
            "receiver_is_minor": False,
            "verdict": "safe",
        },
    ]

    report = summarize(results)

    assert report["counts"] == {"total": 4, "valid": 4, "errors": 0}
    assert report["overall"] == {
        "support": 4,
        "flagged": 2,
        "positive_support": 2,
        "recall": 0.5,
        "fnr": 0.5,
        "boundary_support": 2,
        "fpr": 0.5,
    }
    assert report["by_subcategory"]["isolation"]["recall"] == 1.0
    assert report["by_subcategory"]["dependency"]["fnr"] == 1.0
    assert report["by_receiver"]["minor"]["fpr"] == 1.0


def test_invalid_verdict_is_error_not_safe():
    report = summarize(
        [
            {
                "case_id": "bad-response",
                "expected_risk": True,
                "subcategory": "combined",
                "receiver_is_minor": False,
                "verdict": None,
                "error": "invalid verdict",
            }
        ]
    )

    assert report["counts"] == {"total": 1, "valid": 0, "errors": 1}
    assert report["overall"]["positive_support"] == 0
    assert report["overall"]["recall"] is None


def test_invalid_case_is_rejected():
    with pytest.raises(ValueError, match="expected_risk"):
        validate_case(
            {
                "case_id": "missing-label",
                "text": "테스트",
                "subcategory": "combined",
                "receiver_is_minor": False,
            }
        )
