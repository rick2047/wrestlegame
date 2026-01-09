"""Tests for wrestler selection modal behavior."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from domain.match_types import MatchTypeDefinition, MatchTypeModifiers
from domain.models import Wrestler
from ui.selector import SelectorScreen


@dataclass
class DummyListView:
    """Minimal stand-in for ListView with a selected index."""

    index: Optional[int]


@dataclass
class DummyDetail:
    """Capture detail panel updates."""

    value: str = ""

    def update(self, text: str) -> None:
        self.value = text


def _build_match_types() -> dict[str, MatchTypeDefinition]:
    return {
        "singles": MatchTypeDefinition(
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
        )
    }


def test_selector_blocks_locked_choice() -> None:
    """Locked wrestler should not be selectable."""
    roster = {
        "a": Wrestler("a", "A", "Face", 50, 50, {"singles"}),
        "b": Wrestler("b", "B", "Heel", 50, 50, set()),
    }
    match_types = _build_match_types()
    screen = SelectorScreen(roster, "A", "a", "singles", match_types)
    screen._order = ["a", "b"]
    dummy_list = DummyListView(index=0)
    dummy_detail = DummyDetail()
    notices: list[str] = []
    dismissed: list[Optional[str]] = []

    def query_one(selector: str, _type=None):
        return dummy_list if selector == "#roster-list" else dummy_detail

    screen.query_one = query_one  # type: ignore[assignment]
    screen.notify = lambda message, **kwargs: notices.append(message)  # type: ignore[assignment]
    screen.dismiss = lambda value=None: dismissed.append(value)  # type: ignore[assignment]

    screen.action_select()

    assert notices
    assert dismissed == []


def test_selector_updates_detail_with_proficiency() -> None:
    """Detail panel should include match type proficiency label."""
    roster = {
        "a": Wrestler("a", "A", "Face", 50, 50, {"singles"}),
    }
    match_types = _build_match_types()
    screen = SelectorScreen(roster, "A", None, "singles", match_types)
    screen._order = ["a"]
    dummy_list = DummyListView(index=0)
    dummy_detail = DummyDetail()

    def query_one(selector: str, _type=None):
        return dummy_list if selector == "#roster-list" else dummy_detail

    screen.query_one = query_one  # type: ignore[assignment]

    screen._update_detail()

    assert "Singles" in dummy_detail.value
    assert "Proficiency" in dummy_detail.value
