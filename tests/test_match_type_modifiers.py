"""Tests for match type modifiers and audit fields in results."""

from __future__ import annotations

from domain.match_types import MatchTypeDefinition, MatchTypeModifiers
from domain.models import Match, Wrestler
from sim.engine import simulate_match


def test_match_result_includes_match_type_audit_fields() -> None:
    """Match results should include match type identity and applied modifiers."""
    roster = {
        "a": Wrestler("a", "A", "Face", 60, 80),
        "b": Wrestler("b", "B", "Heel", 55, 75),
    }
    match_types = {
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
    match = Match("a", "b", "singles")
    result = simulate_match(match, roster, match_types, seed=11)
    assert result.match_type_id == "singles"
    assert result.match_type_name == "Singles"
    assert result.applied_modifiers == match_types["singles"].modifiers.as_dict()


def test_match_type_modifiers_change_outcomes() -> None:
    """Different modifiers should yield different ratings or deltas."""
    roster = {
        "a": Wrestler("a", "A", "Face", 60, 80),
        "b": Wrestler("b", "B", "Heel", 55, 75),
    }
    base_modifiers = MatchTypeModifiers(
        rating_bonus=0,
        rating_variance=5,
        stamina_cost_winner=10,
        stamina_cost_loser=12,
        popularity_delta_winner=4,
        popularity_delta_loser=-2,
    )
    extreme_modifiers = MatchTypeModifiers(
        rating_bonus=10,
        rating_variance=5,
        stamina_cost_winner=20,
        stamina_cost_loser=22,
        popularity_delta_winner=8,
        popularity_delta_loser=-4,
    )
    match_types = {
        "base": MatchTypeDefinition("base", "Base", None, base_modifiers),
        "extreme": MatchTypeDefinition("extreme", "Extreme", None, extreme_modifiers),
    }
    match_base = Match("a", "b", "base")
    match_extreme = Match("a", "b", "extreme")
    result_base = simulate_match(match_base, roster, match_types, seed=5)
    result_extreme = simulate_match(match_extreme, roster, match_types, seed=5)
    assert (
        result_base.rating != result_extreme.rating
        or result_base.deltas != result_extreme.deltas
    )
