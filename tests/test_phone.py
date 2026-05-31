import pytest

from app.core.phone import normalize_phone, validate_phone


@pytest.mark.parametrize("raw", [
    "+79001234567",
    "79001234567",
    "89001234567",
    "9001234567",
    "+7 (900) 123-45-67",
    "8 900 123 45 67",
    "8-900-123-45-67",
])
def test_validate_accepts_valid(raw):
    assert validate_phone(raw) is True


@pytest.mark.parametrize("raw", [
    "",
    "123",
    "+7900123456",        # на одну цифру меньше
    "+790012345678",      # на одну цифру больше
    "abcdefghij",
    "+1 202 555 0123",    # не RF-формат
])
def test_validate_rejects_invalid(raw):
    assert validate_phone(raw) is False


@pytest.mark.parametrize("raw", [
    "+79001234567",
    "79001234567",
    "89001234567",
    "9001234567",
    "+7 (900) 123-45-67",
    "8 900 123 45 67",
])
def test_normalize_canonical_form(raw):
    assert normalize_phone(raw) == "+79001234567"


def test_normalize_is_idempotent():
    once = normalize_phone("8 (900) 123-45-67")
    assert normalize_phone(once) == once
