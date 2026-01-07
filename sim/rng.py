from __future__ import annotations

import random


class RNG:
    def __init__(self, seed: int) -> None:
        self._rng = random.Random(seed)

    def randint(self, low: int, high: int) -> int:
        return self._rng.randint(low, high)

    def weighted_choice(self, a_id: str, a_weight: int, b_id: str, b_weight: int) -> str:
        total = max(1, a_weight + b_weight)
        roll = self._rng.randint(1, total)
        return a_id if roll <= a_weight else b_id
