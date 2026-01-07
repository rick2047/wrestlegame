from __future__ import annotations

from domain.booking import is_valid_booking
from domain.models import Match, MatchResult, StatDelta, Wrestler, clamp_stat
from domain.roster import seed_roster
from sim.engine import apply_result, simulate_match
from sim.rng import RNG


def test_clamp_stat_bounds() -> None:
    assert clamp_stat(-5) == 0
    assert clamp_stat(0) == 0
    assert clamp_stat(100) == 100
    assert clamp_stat(120) == 100


def test_wrestler_clamps_on_init() -> None:
    wrestler = Wrestler("test", "Test", "Face", 120, -10)
    assert wrestler.popularity == 100
    assert wrestler.stamina == 0


def test_is_valid_booking() -> None:
    assert is_valid_booking(None, None) is False
    assert is_valid_booking("a", None) is False
    assert is_valid_booking(None, "b") is False
    assert is_valid_booking("a", "a") is False
    assert is_valid_booking("a", "b") is True


def test_rng_determinism() -> None:
    rng_a = RNG(42)
    rng_b = RNG(42)
    rolls_a = [rng_a.randint(1, 10) for _ in range(5)]
    rolls_b = [rng_b.randint(1, 10) for _ in range(5)]
    assert rolls_a == rolls_b


def test_simulate_match_deterministic() -> None:
    roster = seed_roster()
    match = Match("asha", "rohan")
    result_a = simulate_match(match, roster, seed=10)
    result_b = simulate_match(match, roster, seed=10)
    assert result_a == result_b


def test_simulate_match_has_both_deltas() -> None:
    roster = seed_roster()
    match = Match("asha", "rohan")
    result = simulate_match(match, roster, seed=3)
    assert set(result.deltas.keys()) == {"asha", "rohan"}


def test_rating_is_within_bounds() -> None:
    roster = seed_roster()
    match = Match("asha", "rohan")
    result = simulate_match(match, roster, seed=7)
    assert 0 <= result.rating <= 100


def test_apply_result_clamps_stats() -> None:
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


def test_seed_roster_unique_ids() -> None:
    roster = seed_roster()
    assert len(roster.keys()) == len(set(roster.keys()))
