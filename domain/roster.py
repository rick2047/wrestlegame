"""Seed roster data for the vertical slice."""

from __future__ import annotations

from typing import Dict

from domain.models import Wrestler


def seed_roster() -> Dict[str, Wrestler]:
    """Return a small, hard-coded roster with mixed alignments."""
    wrestlers = [
        Wrestler(
            "asha",
            "Asha Blaze",
            "Face",
            48,
            90,
            {"singles", "submission", "iron_man"},
        ),
        Wrestler(
            "rohan",
            "Rohan Steel",
            "Heel",
            52,
            85,
            {"singles", "steel_cage", "hardcore"},
        ),
        Wrestler(
            "mina",
            "Mina Kage",
            "Heel",
            44,
            76,
            {"singles", "ladder", "no_dq"},
        ),
        Wrestler(
            "leo",
            "Leo Nova",
            "Face",
            61,
            70,
            {"singles", "tlc", "ladder"},
        ),
        Wrestler(
            "jax",
            "Jax Thunder",
            "Face",
            57,
            82,
            {"singles", "falls_count_anywhere", "hardcore"},
        ),
        Wrestler(
            "ivy",
            "Ivy Wren",
            "Heel",
            50,
            66,
            {"singles", "submission", "steel_cage"},
        ),
        Wrestler(
            "ember",
            "Ember Vale",
            "Face",
            55,
            74,
            {"singles", "iron_man", "last_man_standing"},
        ),
        Wrestler(
            "goro",
            "Goro Wolfe",
            "Heel",
            63,
            68,
            {"singles", "hardcore", "no_dq"},
        ),
    ]
    return {wrestler.id: wrestler for wrestler in wrestlers}
