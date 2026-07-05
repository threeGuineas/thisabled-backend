"""만 나이·연령대·쌍 정규화 유틸 (§4.5, MATCH-02-5)."""

import uuid
from datetime import date

from app.core.age import age_band, full_age, is_minor
from app.core.pairs import normalize_pair

TODAY = date(2026, 7, 5)


def test_full_age_boundaries():
    # 생일 당일 = 만 나이 +1, 전날은 아직
    assert full_age(date(2012, 7, 5), TODAY) == 14
    assert full_age(date(2012, 7, 6), TODAY) == 13
    assert full_age(date(2000, 1, 1), TODAY) == 26


def test_is_minor_range():
    # 만 14~18 = 미성년 보호 대상 (§4.5)
    assert is_minor(date(2012, 7, 5), TODAY)  # 만 14
    assert is_minor(date(2008, 7, 6), TODAY)  # 만 17
    assert is_minor(date(2007, 7, 6), TODAY)  # 만 18
    assert not is_minor(date(2007, 7, 5), TODAY)  # 만 19
    assert not is_minor(date(2013, 7, 5), TODAY)  # 만 13 (가입 불가 연령)


def test_age_band_boundaries():
    assert age_band(date(2012, 7, 5), TODAY) == "14-18"
    assert age_band(date(2007, 7, 5), TODAY) == "19-24"
    assert age_band(date(2001, 7, 5), TODAY) == "25-34"
    assert age_band(date(1991, 7, 5), TODAY) == "35-44"
    assert age_band(date(1981, 7, 5), TODAY) == "45-54"
    assert age_band(date(1971, 7, 5), TODAY) == "55+"


def test_normalize_pair_orders_by_uuid():
    a = uuid.UUID("00000000-0000-0000-0000-000000000001")
    b = uuid.UUID("00000000-0000-0000-0000-000000000002")
    assert normalize_pair(b, a) == (a, b)
    assert normalize_pair(a, b) == (a, b)
