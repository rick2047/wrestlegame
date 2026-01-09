"""Tests for booking validation rules."""

from __future__ import annotations

from domain.booking import is_valid_booking
from domain.match_types import load_match_types


def test_is_valid_booking() -> None:
    """Booking requires two distinct, non-empty IDs."""
    match_types = load_match_types()
    match_type = next(iter(match_types.keys()))
    assert is_valid_booking(None, None, match_type) is False
    assert is_valid_booking("a", None, match_type) is False
    assert is_valid_booking(None, "b", match_type) is False
    assert is_valid_booking("a", "a", match_type) is False
    assert is_valid_booking("a", "b", None) is False
    assert is_valid_booking("a", "b", match_type, set(match_types.keys())) is True


def test_is_valid_booking_rejects_unknown_match_type() -> None:
    """Booking should reject unknown match type IDs."""
    match_types = load_match_types()
    assert is_valid_booking("a", "b", "unknown", set(match_types.keys())) is False
