"""COMM 외부 응답은 JSON/Markdown 형식과 무관하게 평문 후보만 노출한다."""

import pytest

from app.services.comm import _plain_text, _suggestions, _text_result


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (
            '```json\n["안녕하세요.", "반가워요."]\n```',
            ["안녕하세요.", "반가워요."],
        ),
        (
            '```json\n{"suggestions":["좋아요!", "고마워요"]}\n```',
            ["좋아요!", "고마워요"],
        ),
        (
            "```json\n[\n{\n\"suggestions\": [\"천천히 말해 주세요\"]\n}\n]\n```",
            ["천천히 말해 주세요"],
        ),
        ("1. **안녕하세요**\n2. `반가워요`", ["안녕하세요", "반가워요"]),
    ],
)
def test_suggestions_are_plain_text(raw, expected):
    assert _suggestions(raw, limit=3) == expected


def test_plain_text_removes_code_fence():
    assert _plain_text("```text\n쉬운 문장입니다.\n```") == "쉬운 문장입니다."


def test_text_result_extracts_plain_text_from_fenced_json():
    assert _text_result('```json\n{"result":"쉬운 문장입니다."}\n```') == "쉬운 문장입니다."


def test_suggestions_drop_json_delimiters_in_fallback():
    assert _suggestions("```json\n[\n{\n}\n]\n```", limit=3) == []
