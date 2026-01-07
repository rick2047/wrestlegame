"""Core domain models for wrestlers and match results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal

Alignment = Literal["Face", "Heel"]


def clamp_stat(value: int) -> int:
    """Clamp a stat to the 0-100 range."""
    return max(0, min(100, value))


@dataclass
class Wrestler:
    """Represents a wrestler with alignment and core stats."""
    id: str
    name: str
    alignment: Alignment
    popularity: int
    stamina: int

    def __post_init__(self) -> None:
        """Normalize stats on creation."""
        self.popularity = clamp_stat(self.popularity)
        self.stamina = clamp_stat(self.stamina)


@dataclass(frozen=True)
class Match:
    """Represents a booked match between two wrestlers."""
    wrestler_a_id: str
    wrestler_b_id: str


@dataclass(frozen=True)
class StatDelta:
    """Represents stat changes for a wrestler after a match."""
    popularity: int
    stamina: int


@dataclass(frozen=True)
class MatchResult:
    """Represents the outcome of a simulated match."""
    winner_id: str
    loser_id: str
    rating: int
    deltas: Dict[str, StatDelta]
