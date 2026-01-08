"""Tests for booking validation rules."""

from __future__ import annotations

from domain.booking import is_valid_booking
from domain.match_types import MATCH_TYPES


def test_is_valid_booking() -> None:
    """Booking requires two distinct, non-empty IDs."""
    match_type = MATCH_TYPES[0].id
    assert is_valid_booking(None, None, match_type) is False
    assert is_valid_booking("a", None, match_type) is False
    assert is_valid_booking(None, "b", match_type) is False
    assert is_valid_booking("a", "a", match_type) is False
    assert is_valid_booking("a", "b", None) is False
    assert is_valid_booking("a", "b", match_type) is True
