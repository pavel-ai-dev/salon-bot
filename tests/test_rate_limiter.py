import pytest

from app.core import rate_limiter
from app.core.rate_limiter import RateLimiter


@pytest.fixture
def clock(monkeypatch):
    """Управляемое монотонное время для rate_limiter."""
    state = {"t": 1000.0}
    monkeypatch.setattr(rate_limiter.time, "monotonic", lambda: state["t"])
    return state


def test_allows_up_to_limit(clock):
    rl = RateLimiter(limit=3, window=60)
    assert rl.check(1) == (True, 0)
    assert rl.check(1) == (True, 0)
    assert rl.check(1) == (True, 0)


def test_blocks_over_limit_with_wait(clock):
    rl = RateLimiter(limit=2, window=60)
    rl.check(1)
    rl.check(1)
    ok, wait = rl.check(1)
    assert ok is False
    assert wait >= 1


def test_users_are_independent(clock):
    rl = RateLimiter(limit=1, window=60)
    assert rl.check(1)[0] is True
    assert rl.check(2)[0] is True   # другой пользователь не задет
    assert rl.check(1)[0] is False


def test_window_slides_and_frees_slot(clock):
    rl = RateLimiter(limit=1, window=10)
    assert rl.check(1) == (True, 0)
    assert rl.check(1)[0] is False
    clock["t"] += 11               # окно прошло
    assert rl.check(1) == (True, 0)


def test_wait_decreases_as_time_passes(clock):
    rl = RateLimiter(limit=1, window=100)
    rl.check(1)
    _, wait_early = rl.check(1)
    clock["t"] += 50
    _, wait_late = rl.check(1)
    assert wait_late < wait_early
