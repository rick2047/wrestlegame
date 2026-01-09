"""Tests for roster loading fallback behavior."""

from __future__ import annotations

from pathlib import Path

from domain.roster import load_roster


def test_load_roster_fallback_when_missing_file(tmp_path: Path) -> None:
    """Missing roster file should return fallback dataset."""
    missing_path = tmp_path / "missing.json"
    roster = load_roster(missing_path)
    assert len(roster) >= 2


def test_load_roster_fallback_when_empty_file(tmp_path: Path) -> None:
    """Empty roster list should return fallback dataset."""
    roster_path = tmp_path / "wrestlers.json"
    roster_path.write_text("{\"wrestlers\": []}", encoding="utf-8")
    roster = load_roster(roster_path)
    assert len(roster) >= 2


def test_load_roster_fallback_on_invalid_json(tmp_path: Path) -> None:
    """Invalid JSON should return fallback dataset."""
    roster_path = tmp_path / "wrestlers.json"
    roster_path.write_text("{not: valid}", encoding="utf-8")
    roster = load_roster(roster_path)
    assert len(roster) >= 2
