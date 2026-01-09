"""Bounds tests for popularity and stamina clamping."""

from __future__ import annotations

from domain.models import MatchResult, StatDelta, Wrestler
from sim.engine import apply_result


def test_apply_result_clamps_popularity_and_stamina() -> None:
    """Stat deltas must be clamped to the 0-100 range."""
    roster = {
        "a": Wrestler("a", "A", "Face", 100, 2),
        "b": Wrestler("b", "B", "Heel", 0, 1),
    }
    result = MatchResult(
        match_type_id="singles",
        match_type_name="Singles",
        applied_modifiers={},
        winner_id="a",
        loser_id="b",
        rating=80,
        deltas={
            "a": StatDelta(popularity=10, stamina=5),
            "b": StatDelta(popularity=-10, stamina=-5),
        },
    )
    apply_result(roster, result)
    assert roster["a"].popularity == 100
    assert roster["a"].stamina == 7
    assert roster["b"].popularity == 0
    assert roster["b"].stamina == 0
