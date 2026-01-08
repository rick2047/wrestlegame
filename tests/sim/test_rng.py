"""Tests for the deterministic RNG wrapper."""

from __future__ import annotations

from sim.rng import RNG


def test_rng_determinism() -> None:
    """Seeded RNG should produce consistent rolls."""
    rng_a = RNG(42)
    rng_b = RNG(42)
    rolls_a = [rng_a.randint(1, 10) for _ in range(5)]
    rolls_b = [rng_b.randint(1, 10) for _ in range(5)]
    assert rolls_a == rolls_b
