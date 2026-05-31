import pytest

from app.core import callback_dedup
from app.core.callback_dedup import is_duplicate


@pytest.fixture(autouse=True)
def reset_state(monkeypatch):
    """Глобальный _seen — изолируем каждый тест и даём управляемое время."""
    callback_dedup._seen.clear()
    state = {"t": 0.0}
    monkeypatch.setattr(callback_dedup.time, "monotonic", lambda: state["t"])
    yield state
    callback_dedup._seen.clear()


def test_none_is_never_duplicate():
    assert is_duplicate(None) is False


def test_first_seen_then_duplicate():
    assert is_duplicate("cb-1") is False
    assert is_duplicate("cb-1") is True


def test_distinct_ids_not_duplicate():
    assert is_duplicate("a") is False
    assert is_duplicate("b") is False


def test_entry_expires_after_ttl(reset_state):
    assert is_duplicate("cb-1") is False
    reset_state["t"] += callback_dedup._TTL + 1
    # запись протухла → снова не дубликат
    assert is_duplicate("cb-1") is False


def test_eviction_keeps_cache_bounded(reset_state):
    for i in range(callback_dedup._MAX + 50):
        is_duplicate(f"id-{i}")
        reset_state["t"] += 0.001
    assert len(callback_dedup._seen) <= callback_dedup._MAX
