"""Keyboard navigation focus tests for key screens."""

from __future__ import annotations

from typing import Optional

from domain.match_types import MatchTypeDefinition, MatchTypeModifiers
from domain.models import Match, MatchResult, StatDelta, Wrestler
from ui.hub import HubScreen
from ui.match_type_selector import MatchTypeSelectorScreen
from ui.results import ResultsScreen
from ui.selector import SelectorScreen


class FocusProbe:
    """Capture focus changes for focus methods."""

    def __init__(self) -> None:
        self.next_calls = 0
        self.prev_calls = 0

    def focus_next(self) -> None:
        self.next_calls += 1

    def focus_previous(self) -> None:
        self.prev_calls += 1


def _match_types() -> dict[str, MatchTypeDefinition]:
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


def test_hub_focus_actions_call_focus_methods() -> None:
    """Hub focus actions should delegate to focus movement."""
    screen = HubScreen()
    probe = FocusProbe()
    screen.focus_next = probe.focus_next  # type: ignore[assignment]
    screen.focus_previous = probe.focus_previous  # type: ignore[assignment]

    screen.action_focus_next()
    screen.action_focus_previous()

    assert probe.next_calls == 1
    assert probe.prev_calls == 1


def test_selector_focus_actions_call_focus_methods() -> None:
    """Selector focus actions should delegate to focus movement."""
    roster = {"a": Wrestler("a", "A", "Face", 50, 50)}
    screen = SelectorScreen(roster, "A", None, "singles", _match_types())
    probe = FocusProbe()
    screen.focus_next = probe.focus_next  # type: ignore[assignment]
    screen.focus_previous = probe.focus_previous  # type: ignore[assignment]

    screen.action_focus_next()
    screen.action_focus_previous()

    assert probe.next_calls == 1
    assert probe.prev_calls == 1


def test_match_type_selector_focus_actions_call_focus_methods() -> None:
    """Match type selector focus actions should delegate to focus movement."""
    screen = MatchTypeSelectorScreen(list(_match_types().values()))
    probe = FocusProbe()
    screen.focus_next = probe.focus_next  # type: ignore[assignment]
    screen.focus_previous = probe.focus_previous  # type: ignore[assignment]

    screen.action_focus_next()
    screen.action_focus_previous()

    assert probe.next_calls == 1
    assert probe.prev_calls == 1


def test_results_focus_actions_call_focus_methods() -> None:
    """Results focus actions should delegate to focus movement."""
    roster = {
        "a": Wrestler("a", "A", "Face", 50, 50),
        "b": Wrestler("b", "B", "Heel", 50, 50),
    }
    match = Match("a", "b", "singles")
    result = MatchResult(
        match_type_id="singles",
        match_type_name="Singles",
        applied_modifiers={},
        winner_id="a",
        loser_id="b",
        rating=80,
        deltas={
            "a": StatDelta(popularity=1, stamina=-1),
            "b": StatDelta(popularity=-1, stamina=-1),
        },
    )
    screen = ResultsScreen(match, result)
    probe = FocusProbe()
    screen.focus_next = probe.focus_next  # type: ignore[assignment]
    screen.focus_previous = probe.focus_previous  # type: ignore[assignment]

    screen.action_focus_next()
    screen.action_focus_previous()

    assert probe.next_calls == 1
    assert probe.prev_calls == 1
