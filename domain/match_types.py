"""Match type definitions and tuning data."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass(frozen=True)
class MatchTypeModifiers:
    """Represents tuning values for a match type."""

    rating_bonus: int
    rating_variance: int
    stamina_cost_winner: int
    stamina_cost_loser: int
    popularity_delta_winner: int
    popularity_delta_loser: int

    def as_dict(self) -> Dict[str, int]:
        """Return modifiers as a plain dictionary."""
        return {
            "rating_bonus": self.rating_bonus,
            "rating_variance": self.rating_variance,
            "stamina_cost_winner": self.stamina_cost_winner,
            "stamina_cost_loser": self.stamina_cost_loser,
            "popularity_delta_winner": self.popularity_delta_winner,
            "popularity_delta_loser": self.popularity_delta_loser,
        }


@dataclass(frozen=True)
class MatchTypeDefinition:
    """Defines a match type loaded from configuration."""

    id: str
    name: str
    description: Optional[str]
    modifiers: MatchTypeModifiers


_FALLBACK_MATCH_TYPES: List[MatchTypeDefinition] = [
    MatchTypeDefinition(
        id="singles",
        name="Singles",
        description="Standard one-on-one match",
        modifiers=MatchTypeModifiers(
            rating_bonus=0,
            rating_variance=5,
            stamina_cost_winner=10,
            stamina_cost_loser=12,
            popularity_delta_winner=4,
            popularity_delta_loser=-2,
        ),
    )
]


def _parse_match_type(entry: Dict[str, object]) -> MatchTypeDefinition:
    """Build a match type definition from JSON data."""
    modifiers = entry.get("modifiers") or {}
    return MatchTypeDefinition(
        id=str(entry["id"]),
        name=str(entry["name"]),
        description=str(entry["description"]) if entry.get("description") else None,
        modifiers=MatchTypeModifiers(
            rating_bonus=int(modifiers.get("rating_bonus", 0)),
            rating_variance=int(modifiers.get("rating_variance", 0)),
            stamina_cost_winner=int(modifiers.get("stamina_cost_winner", 0)),
            stamina_cost_loser=int(modifiers.get("stamina_cost_loser", 0)),
            popularity_delta_winner=int(modifiers.get("popularity_delta_winner", 0)),
            popularity_delta_loser=int(modifiers.get("popularity_delta_loser", 0)),
        ),
    )


def load_match_types(path: Optional[Path] = None) -> Dict[str, MatchTypeDefinition]:
    """Load match type definitions from JSON, with fallback data."""
    target = path or Path("data/match_types.json")
    if not target.exists():
        return {match_type.id: match_type for match_type in _FALLBACK_MATCH_TYPES}
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
        entries = payload.get("match_types", [])
        if not entries:
            return {match_type.id: match_type for match_type in _FALLBACK_MATCH_TYPES}
        match_types = [_parse_match_type(entry) for entry in entries]
        return {match_type.id: match_type for match_type in match_types}
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
        return {match_type.id: match_type for match_type in _FALLBACK_MATCH_TYPES}


MATCH_TYPE_LOOKUP: Dict[str, MatchTypeDefinition] = load_match_types()
MATCH_TYPES: List[MatchTypeDefinition] = list(MATCH_TYPE_LOOKUP.values())
