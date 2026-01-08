"""Core domain models for wrestlers and match results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Literal, Set

from domain.match_types import MatchType

Alignment = Literal["Face", "Heel"]


def clamp_stat(value: int) -> int:
    """Clamp a stat to the 0-100 range.

    Used for both input normalization and post-match updates.
    """
    return max(0, min(100, value))


@dataclass
class Wrestler:
    """Represents a wrestler used by booking and simulation.

    Stores alignment plus core stats that influence match outcomes.
    Popularity and stamina are clamped to 0-100 on creation.
    """
    id: str
    name: str
    alignment: Alignment
    popularity: int
    stamina: int
    match_type_proficiency: Set[MatchType] = field(default_factory=set)

    def __post_init__(self) -> None:
        """Normalize stats on creation."""
        self.popularity = clamp_stat(self.popularity)
        self.stamina = clamp_stat(self.stamina)

    def is_proficient(self, match_type: MatchType) -> bool:
        """Return True if the wrestler is proficient in the match type."""
        return match_type in self.match_type_proficiency


@dataclass(frozen=True)
class Match:
    """Represents a booked match by wrestler IDs.

    The model is immutable to keep simulation inputs stable.
    """
    wrestler_a_id: str
    wrestler_b_id: str
    match_type: MatchType


@dataclass(frozen=True)
class StatDelta:
    """Represents popularity and stamina changes after a match.

    Deltas are applied to the roster to update long-term state.
    """
    popularity: int
    stamina: int


@dataclass(frozen=True)
class MatchResult:
    """Represents a simulated outcome with explicit deltas.

    The result includes the winner/loser IDs, a rating, and per-wrestler deltas.
    """
    winner_id: str
    loser_id: str
    rating: int
    deltas: Dict[str, StatDelta]
