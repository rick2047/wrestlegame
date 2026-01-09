"""Determinism tests for simulation outcomes."""

from __future__ import annotations

from domain.match_types import load_match_types
from domain.models import Match
from domain.roster import seed_roster
from sim.engine import simulate_match


def test_simulation_is_deterministic_for_same_seed() -> None:
    """Same inputs and seed should yield identical results."""
    roster = seed_roster()
    match_types = load_match_types()
    match = Match("john_steel", "max_power", "singles")
    result_a = simulate_match(match, roster, match_types, seed=42)
    result_b = simulate_match(match, roster, match_types, seed=42)
    assert result_a == result_b
