"""만 나이 계산 (§4.5 미성년 보호, MATCH-02-5 연령대).

생년월일 원문은 저장만 하고 파생값(만 나이·연령대·미성년)은 항상 요청 시점에 계산한다.
"""

from datetime import date

# MATCH-02-5 연령대 구간: (상한 만 나이, 라벨)
_BANDS = [(18, "14-18"), (24, "19-24"), (34, "25-34"), (44, "35-44"), (54, "45-54")]

MINOR_MIN = 14  # 최소 가입 연령 (§4.1)
MINOR_MAX = 18  # 미성년 보호 상한 (§4.5)


def full_age(birth_date: date, today: date | None = None) -> int:
    """만 나이. 생일 당일부터 +1."""
    today = today or date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def is_minor(birth_date: date, today: date | None = None) -> bool:
    """만 14~18세 미성년 보호 대상 여부 (§4.5). 만 13 이하는 가입 자체가 불가."""
    return MINOR_MIN <= full_age(birth_date, today) <= MINOR_MAX


def age_band(birth_date: date, today: date | None = None) -> str:
    """MATCH-02-5 연령대. 추천 특성으로만 사용, 생년월일 원문은 모델에 전달하지 않는다."""
    age = full_age(birth_date, today)
    for upper, label in _BANDS:
        if age <= upper:
            return label
    return "55+"
