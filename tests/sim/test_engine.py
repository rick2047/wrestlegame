"""Tests for the match simulation engine."""

from __future__ import annotations

from domain.models import Match, MatchResult, StatDelta, Wrestler
from domain.roster import seed_roster
from sim.engine import apply_result, simulate_match


def test_simulate_match_deterministic() -> None:
    """Simulated results should be identical for the same seed."""
    roster = seed_roster()
    match = Match("asha", "rohan")
    result_a = simulate_match(match, roster, seed=10)
    result_b = simulate_match(match, roster, seed=10)
    assert result_a == result_b


def test_simulate_match_has_both_deltas() -> None:
    """Match results should include deltas for both wrestlers."""
    roster = seed_roster()
    match = Match("asha", "rohan")
    result = simulate_match(match, roster, seed=3)
    assert set(result.deltas.keys()) == {"asha", "rohan"}


def test_rating_is_within_bounds() -> None:
    """Ratings should always be clamped to 0-100."""
    roster = seed_roster()
    match = Match("asha", "rohan")
    result = simulate_match(match, roster, seed=7)
    assert 0 <= result.rating <= 100


def test_apply_result_clamps_stats() -> None:
    """Applying results should clamp stats to valid bounds."""
    roster = {
        "a": Wrestler("a", "A", "Face", 100, 2),
        "b": Wrestler("b", "B", "Heel", 0, 1),
    }
    result = MatchResult(
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

