"""Deterministic RNG wrapper for simulation."""

from __future__ import annotations

import random


class RNG:
    """Seeded RNG helper used by the simulation engine.

    Provides predictable randomness for tests and repeatable match results.
    Includes a weighted_choice helper so win odds can be based on stats.
    """
    def __init__(self, seed: int) -> None:
        """Create a new RNG with a fixed seed."""
        self._rng = random.Random(seed)

    def randint(self, low: int, high: int) -> int:
        """Return a random integer between low and high, inclusive."""
        return self._rng.randint(low, high)

    def weighted_choice(self, a_id: str, a_weight: int, b_id: str, b_weight: int) -> str:
        """Pick a_id or b_id based on the provided weights."""
        total = max(1, a_weight + b_weight)
        roll = self._rng.randint(1, total)
        return a_id if roll <= a_weight else b_id
