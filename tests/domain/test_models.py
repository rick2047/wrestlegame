"""Tests for domain models and stat clamping."""

from __future__ import annotations

from domain.models import Wrestler, clamp_stat


def test_clamp_stat_bounds() -> None:
    """Clamp should respect lower and upper bounds."""
    assert clamp_stat(-5) == 0
    assert clamp_stat(0) == 0
    assert clamp_stat(100) == 100
    assert clamp_stat(120) == 100


def test_wrestler_clamps_on_init() -> None:
    """Wrestler should normalize stats on initialization."""
    wrestler = Wrestler("test", "Test", "Face", 120, -10)
    assert wrestler.popularity == 100
    assert wrestler.stamina == 0
