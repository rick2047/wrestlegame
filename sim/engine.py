from __future__ import annotations

from typing import Dict

from domain.models import Match, MatchResult, StatDelta, Wrestler, clamp_stat
from sim.rng import RNG


def simulate_match(match: Match, roster: Dict[str, Wrestler], seed: int) -> MatchResult:
    rng = RNG(seed)
    wrestler_a = roster[match.wrestler_a_id]
    wrestler_b = roster[match.wrestler_b_id]

    a_weight = wrestler_a.popularity + wrestler_a.stamina + rng.randint(-5, 5)
    b_weight = wrestler_b.popularity + wrestler_b.stamina + rng.randint(-5, 5)
    winner_id = rng.weighted_choice(
        wrestler_a.id, max(1, a_weight), wrestler_b.id, max(1, b_weight)
    )
    loser_id = wrestler_b.id if winner_id == wrestler_a.id else wrestler_a.id

    base = (wrestler_a.popularity + wrestler_b.popularity) / 2
    bonus = 5 if wrestler_a.alignment != wrestler_b.alignment else 0
    penalty = 0
    if wrestler_a.stamina < 40:
        penalty -= 5
    if wrestler_b.stamina < 40:
        penalty -= 5
    variance = rng.randint(-5, 5)
    rating = clamp_stat(int(base + bonus + penalty + variance))

    winner_popularity = 3
    loser_popularity = -1
    stamina_loss = 8 + rng.randint(0, 4)

    deltas = {
        winner_id: StatDelta(popularity=winner_popularity, stamina=-stamina_loss),
        loser_id: StatDelta(popularity=loser_popularity, stamina=-stamina_loss),
    }

    return MatchResult(
        winner_id=winner_id,
        loser_id=loser_id,
        rating=rating,
        deltas=deltas,
    )


def apply_result(roster: Dict[str, Wrestler], result: MatchResult) -> None:
    for wrestler_id, delta in result.deltas.items():
        wrestler = roster[wrestler_id]
        wrestler.popularity = clamp_stat(wrestler.popularity + delta.popularity)
        wrestler.stamina = clamp_stat(wrestler.stamina + delta.stamina)
