from datetime import datetime, timezone

import pytest

from app.core import time_utils
from app.core.time_utils import (
    booking_dates,
    fmt_date,
    fmt_date_btn,
    parse_dt,
    to_utc,
)


def test_fmt_date_known_monday():
    # 2024-01-01 — понедельник
    assert fmt_date("2024-01-01") == "01.01.2024 (пн)"


def test_fmt_date_btn_human_form():
    assert fmt_date_btn("2024-01-01") == "Понедельник, 1 января"


def test_to_utc_moscow_offset():
    # Europe/Moscow = UTC+3 круглый год (без DST)
    dt = to_utc("2026-01-15", "12:00")
    assert dt.tzinfo is not None
    assert dt.hour == 9
    assert dt.year == 2026 and dt.month == 1 and dt.day == 15


def test_parse_dt_none_and_invalid():
    assert parse_dt(None) is None
    assert parse_dt("") is None
    assert parse_dt("не дата") is None


def test_parse_dt_z_suffix_is_utc():
    dt = parse_dt("2026-01-01T00:00:00Z")
    assert dt == datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_booking_dates_window(monkeypatch):
    from datetime import date as _date

    monkeypatch.setattr(time_utils, "local_today", lambda: _date(2026, 1, 10))
    dates = booking_dates()
    assert dates[0] == "2026-01-11"          # начинается с завтра
    assert len(dates) == time_utils.settings.BOOKING_WINDOW_DAYS
    assert dates == sorted(dates)            # по возрастанию
