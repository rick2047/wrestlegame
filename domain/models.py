from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal

Alignment = Literal["Face", "Heel"]


def clamp_stat(value: int) -> int:
    return max(0, min(100, value))


@dataclass
class Wrestler:
    id: str
    name: str
    alignment: Alignment
    popularity: int
    stamina: int

    def __post_init__(self) -> None:
        self.popularity = clamp_stat(self.popularity)
        self.stamina = clamp_stat(self.stamina)


@dataclass(frozen=True)
class Match:
    wrestler_a_id: str
    wrestler_b_id: str


@dataclass(frozen=True)
class StatDelta:
    popularity: int
    stamina: int


@dataclass(frozen=True)
class MatchResult:
    winner_id: str
    loser_id: str
    rating: int
    deltas: Dict[str, StatDelta]
