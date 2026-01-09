"""Seed roster data for the vertical slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, Optional

from domain.models import Wrestler


_FALLBACK_WRESTLERS = [
    Wrestler("john_steel", "John Steel", "Face", 75, 80),
    Wrestler("max_power", "Max Power", "Heel", 68, 85),
]


def _build_wrestlers(entries: Iterable[Dict[str, object]]) -> Dict[str, Wrestler]:
    """Build a roster dictionary from raw JSON entries."""
    roster: Dict[str, Wrestler] = {}
    for entry in entries:
        proficiency = set(entry.get("proficiency", []) or [])
        wrestler = Wrestler(
            str(entry["id"]),
            str(entry["name"]),
            str(entry["alignment"]),
            int(entry["popularity"]),
            int(entry["stamina"]),
            proficiency,
        )
        roster[wrestler.id] = wrestler
    return roster


def load_roster(path: Optional[Path] = None) -> Dict[str, Wrestler]:
    """Load roster data from JSON, with fallback data."""
    target = path or Path("data/wrestlers.json")
    if not target.exists():
        return {wrestler.id: wrestler for wrestler in _FALLBACK_WRESTLERS}
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
        entries = payload.get("wrestlers", [])
        if not entries:
            return {wrestler.id: wrestler for wrestler in _FALLBACK_WRESTLERS}
        return _build_wrestlers(entries)
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
        return {wrestler.id: wrestler for wrestler in _FALLBACK_WRESTLERS}


def seed_roster() -> Dict[str, Wrestler]:
    """Return the loaded roster (or fallback)."""
    return load_roster()
