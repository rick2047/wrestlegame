"""Tests for the match simulation engine."""

from __future__ import annotations

from domain.match_types import load_match_types
from domain.models import Match, MatchResult, StatDelta, Wrestler
from domain.roster import seed_roster
from sim.engine import apply_result, simulate_match


def test_simulate_match_deterministic() -> None:
    """Simulated results should be identical for the same seed."""
    roster = seed_roster()
    match_types = load_match_types()
    match = Match("john_steel", "max_power", "singles")
    result_a = simulate_match(match, roster, match_types, seed=10)
    result_b = simulate_match(match, roster, match_types, seed=10)
    assert result_a == result_b


def test_simulate_match_has_both_deltas() -> None:
    """Match results should include deltas for both wrestlers."""
    roster = seed_roster()
    match_types = load_match_types()
    match = Match("john_steel", "max_power", "singles")
    result = simulate_match(match, roster, match_types, seed=3)
    assert set(result.deltas.keys()) == {"john_steel", "max_power"}


def test_rating_is_within_bounds() -> None:
    """Ratings should always be clamped to 0-100."""
    roster = seed_roster()
    match_types = load_match_types()
    match = Match("john_steel", "max_power", "singles")
    result = simulate_match(match, roster, match_types, seed=7)
    assert 0 <= result.rating <= 100


def test_apply_result_clamps_stats() -> None:
    """Applying results should clamp stats to valid bounds."""
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


def test_match_type_affects_rating_and_stamina() -> None:
    """Match type tuning should affect rating and stamina loss."""
    roster = {
        "a": Wrestler("a", "A", "Face", 55, 80, set()),
        "b": Wrestler("b", "B", "Heel", 55, 80, set()),
    }
    match_types = load_match_types()
    match_singles = Match("a", "b", "singles")
    match_hardcore = Match("a", "b", "hardcore")
    result_singles = simulate_match(match_singles, roster, match_types, seed=9)
    result_hardcore = simulate_match(match_hardcore, roster, match_types, seed=9)
    assert result_singles.rating != result_hardcore.rating
    singles_loss = abs(result_singles.deltas["a"].stamina)
    hardcore_loss = abs(result_hardcore.deltas["a"].stamina)
    assert hardcore_loss > singles_loss


def test_proficiency_reduces_stamina_loss() -> None:
    """Proficient wrestlers should lose less stamina for the same match type."""
    roster_no_pro = {
        "a": Wrestler("a", "A", "Face", 95, 95, set()),
        "b": Wrestler("b", "B", "Heel", 10, 10, set()),
    }
    roster_pro = {
        "a": Wrestler("a", "A", "Face", 95, 95, {"hardcore"}),
        "b": Wrestler("b", "B", "Heel", 10, 10, set()),
    }
    match = Match("a", "b", "hardcore")
    match_types = load_match_types()
    result_no_pro = simulate_match(match, roster_no_pro, match_types, seed=4)
    result_pro = simulate_match(match, roster_pro, match_types, seed=4)
    loss_no_pro = abs(result_no_pro.deltas["a"].stamina)
    loss_pro = abs(result_pro.deltas["a"].stamina)
    assert loss_no_pro - loss_pro == 2
