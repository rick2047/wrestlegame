"""Validation helpers for booking logic."""

from __future__ import annotations

from typing import Optional, Set

def is_valid_booking(
    wrestler_a_id: Optional[str],
    wrestler_b_id: Optional[str],
    match_type_id: Optional[str],
    valid_match_type_ids: Optional[Set[str]] = None,
) -> bool:
    """Return True when both slots are filled, distinct, and match type is set."""
    if not wrestler_a_id or not wrestler_b_id or not match_type_id:
        return False
    if valid_match_type_ids is not None and match_type_id not in valid_match_type_ids:
        return False
    return wrestler_a_id != wrestler_b_id
