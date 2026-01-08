"""Match type definitions and tuning data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal

MatchType = Literal[
    "singles",
    "hardcore",
    "ladder",
    "steel_cage",
    "falls_count_anywhere",
    "submission",
    "iron_man",
    "tlc",
    "last_man_standing",
    "no_dq",
]


@dataclass(frozen=True)
class MatchTypeProfile:
    """Represents tuning values for a match type."""

    id: MatchType
    label: str
    rating_bonus: int
    stamina_cost: int


MATCH_TYPES: List[MatchTypeProfile] = [
    MatchTypeProfile("singles", "Singles", 0, 8),
    MatchTypeProfile("hardcore", "Hardcore", 4, 12),
    MatchTypeProfile("ladder", "Ladder", 5, 13),
    MatchTypeProfile("steel_cage", "Steel Cage", 4, 12),
    MatchTypeProfile("falls_count_anywhere", "Falls Count Anywhere", 3, 11),
    MatchTypeProfile("submission", "Submission", 2, 9),
    MatchTypeProfile("iron_man", "Iron Man", 6, 15),
    MatchTypeProfile("tlc", "TLC", 6, 14),
    MatchTypeProfile("last_man_standing", "Last Man Standing", 5, 13),
    MatchTypeProfile("no_dq", "No DQ", 3, 11),
]

MATCH_TYPE_LOOKUP: Dict[MatchType, MatchTypeProfile] = {
    match_type.id: match_type for match_type in MATCH_TYPES
}
