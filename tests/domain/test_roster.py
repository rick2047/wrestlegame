"""Tests for seeded roster data."""

from __future__ import annotations

from domain.roster import seed_roster


def test_seed_roster_unique_ids() -> None:
    """Roster IDs should be unique."""
    roster = seed_roster()
    assert len(roster.keys()) == len(set(roster.keys()))
