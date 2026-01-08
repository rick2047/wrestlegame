"""Match simulation engine and stat application."""

from __future__ import annotations

from typing import Dict

from domain.match_types import MATCH_TYPE_LOOKUP
from domain.models import Match, MatchResult, StatDelta, Wrestler, clamp_stat
from sim.rng import RNG


def simulate_match(match: Match, roster: Dict[str, Wrestler], seed: int) -> MatchResult:
    """Simulate a match and return a deterministic MatchResult.

    Inputs:
    - match: the booked pairing by wrestler IDs.
    - roster: lookup table for stats used in weighting and rating.
    - seed: RNG seed to make outcomes reproducible.
    """
    rng = RNG(seed)
    wrestler_a = roster[match.wrestler_a_id]
    wrestler_b = roster[match.wrestler_b_id]

    match_profile = MATCH_TYPE_LOOKUP[match.match_type]
    a_proficient = wrestler_a.is_proficient(match.match_type)
    b_proficient = wrestler_b.is_proficient(match.match_type)

    # Weight outcome by core stats with a small randomness band and proficiency bump.
    a_weight = (
        wrestler_a.popularity
        + wrestler_a.stamina
        + (4 if a_proficient else 0)
        + rng.randint(-5, 5)
    )
    b_weight = (
        wrestler_b.popularity
        + wrestler_b.stamina
        + (4 if b_proficient else 0)
        + rng.randint(-5, 5)
    )
    winner_id = rng.weighted_choice(
        wrestler_a.id, max(1, a_weight), wrestler_b.id, max(1, b_weight)
    )
    loser_id = wrestler_b.id if winner_id == wrestler_a.id else wrestler_a.id

    # Rating blends popularity with alignment bonus, match type, and stamina penalties.
    base = (wrestler_a.popularity + wrestler_b.popularity) / 2
    bonus = 5 if wrestler_a.alignment != wrestler_b.alignment else 0
    if a_proficient and b_proficient:
        proficiency_bonus = 2
    elif a_proficient or b_proficient:
        proficiency_bonus = 1
    else:
        proficiency_bonus = 0
    penalty = 0
    if wrestler_a.stamina < 40:
        penalty -= 5
    if wrestler_b.stamina < 40:
        penalty -= 5
    variance = rng.randint(-5, 5)
    rating = clamp_stat(
        int(base + bonus + match_profile.rating_bonus + proficiency_bonus + penalty + variance)
    )

    # Apply small, bounded deltas so results feel meaningful but stable.
    winner_popularity = 3
    loser_popularity = -1
    stamina_roll = match_profile.stamina_cost + rng.randint(0, 4)
    stamina_loss_a = max(1, stamina_roll - (2 if a_proficient else 0))
    stamina_loss_b = max(1, stamina_roll - (2 if b_proficient else 0))
    stamina_by_id = {
        wrestler_a.id: stamina_loss_a,
        wrestler_b.id: stamina_loss_b,
    }

    deltas = {
        winner_id: StatDelta(
            popularity=winner_popularity,
            stamina=-stamina_by_id[winner_id],
        ),
        loser_id: StatDelta(
            popularity=loser_popularity,
            stamina=-stamina_by_id[loser_id],
        ),
    }

    return MatchResult(
        winner_id=winner_id,
        loser_id=loser_id,
        rating=rating,
        deltas=deltas,
    )


def apply_result(roster: Dict[str, Wrestler], result: MatchResult) -> None:
    """Apply stat deltas to the roster while clamping results.

    This mutates the roster in-place to reflect post-match stat changes.
    """
    for wrestler_id, delta in result.deltas.items():
        wrestler = roster[wrestler_id]
        wrestler.popularity = clamp_stat(wrestler.popularity + delta.popularity)
        wrestler.stamina = clamp_stat(wrestler.stamina + delta.stamina)
