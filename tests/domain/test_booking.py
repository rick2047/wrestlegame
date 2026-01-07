"""Tests for booking validation rules."""

from __future__ import annotations

from domain.booking import is_valid_booking


def test_is_valid_booking() -> None:
    """Booking requires two distinct, non-empty IDs."""
    assert is_valid_booking(None, None) is False
    assert is_valid_booking("a", None) is False
    assert is_valid_booking(None, "b") is False
    assert is_valid_booking("a", "a") is False
    assert is_valid_booking("a", "b") is True
