"""Validation helpers for booking logic."""

from __future__ import annotations

from typing import Optional

from domain.match_types import MatchType


def is_valid_booking(
    wrestler_a_id: Optional[str],
    wrestler_b_id: Optional[str],
    match_type: Optional[MatchType],
) -> bool:
    """Return True when both slots are filled, distinct, and match type is set."""
    if not wrestler_a_id or not wrestler_b_id or not match_type:
        return False
    return wrestler_a_id != wrestler_b_id
