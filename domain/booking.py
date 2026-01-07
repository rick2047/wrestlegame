from __future__ import annotations

from typing import Optional


def is_valid_booking(wrestler_a_id: Optional[str], wrestler_b_id: Optional[str]) -> bool:
    if not wrestler_a_id or not wrestler_b_id:
        return False
    return wrestler_a_id != wrestler_b_id
