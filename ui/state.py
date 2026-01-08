"""Shared UI state for screen transitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from domain.match_types import MatchType
from domain.models import Match, MatchResult


@dataclass
class AppState:
    """Holds selection and simulation state across screens.

    Tracks selected wrestler IDs, the last simulated match/result, and RNG seed
    used by the simulation engine.
    """
    selected_a_id: Optional[str] = None
    selected_b_id: Optional[str] = None
    selected_match_type: Optional[MatchType] = None
    last_match: Optional[Match] = None
    last_result: Optional[MatchResult] = None
    seed: int = 1
