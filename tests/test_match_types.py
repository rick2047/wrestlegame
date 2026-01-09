"""Tests for match type selection modal behavior."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from domain.match_types import MatchTypeDefinition, MatchTypeModifiers
from ui.match_type_selector import MatchTypeSelectorScreen


@dataclass
class DummyListView:
    """Minimal stand-in for ListView with a selected index."""

    index: Optional[int]


def _match_types() -> list[MatchTypeDefinition]:
    return [
        MatchTypeDefinition(
            id="singles",
            name="Singles",
            description=None,
            modifiers=MatchTypeModifiers(
                rating_bonus=0,
                rating_variance=5,
                stamina_cost_winner=10,
                stamina_cost_loser=12,
                popularity_delta_winner=4,
                popularity_delta_loser=-2,
            ),
        ),
        MatchTypeDefinition(
            id="hardcore",
            name="Hardcore",
            description=None,
            modifiers=MatchTypeModifiers(
                rating_bonus=10,
                rating_variance=18,
                stamina_cost_winner=20,
                stamina_cost_loser=22,
                popularity_delta_winner=8,
                popularity_delta_loser=-4,
            ),
        ),
    ]


def test_match_type_selector_returns_selected_id() -> None:
    """Action select should dismiss with the highlighted match type ID."""
    screen = MatchTypeSelectorScreen(_match_types())
    screen._order = ["singles", "hardcore"]
    dummy_list = DummyListView(index=1)
    dismissed: list[Optional[str]] = []

    def query_one(selector: str, _type=None):
        return dummy_list

    screen.query_one = query_one  # type: ignore[assignment]
    screen.dismiss = lambda value=None: dismissed.append(value)  # type: ignore[assignment]

    screen.action_select()

    assert dismissed == ["hardcore"]
