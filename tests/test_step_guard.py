import pytest

from app.core import step_guard
from app.core.step_guard import is_step_expired, set_step


@pytest.fixture
def clock(monkeypatch):
    state = {"t": 500.0}
    monkeypatch.setattr(step_guard.time, "monotonic", lambda: state["t"])
    return state


def test_set_step_records_timestamp(clock):
    d = {}
    set_step(d, "await_phone")
    assert d["step"] == "await_phone"
    assert d["step_ts"] == 500.0


def test_set_step_none_clears_timestamp(clock):
    d = {}
    set_step(d, "await_phone")
    set_step(d, None)
    assert d["step"] is None
    assert "step_ts" not in d


def test_not_expired_without_step(clock):
    assert is_step_expired({}) is False


def test_not_expired_when_step_set_but_no_ts(clock):
    assert is_step_expired({"step": "x"}) is False


def test_not_expired_within_timeout(clock):
    d = {}
    set_step(d, "x")
    clock["t"] += step_guard.STEP_TIMEOUT_SECONDS - 1
    assert is_step_expired(d) is False


def test_expired_after_timeout(clock):
    d = {}
    set_step(d, "x")
    clock["t"] += step_guard.STEP_TIMEOUT_SECONDS + 1
    assert is_step_expired(d) is True
