from __future__ import annotations

from typing import Dict

from domain.models import Wrestler


def seed_roster() -> Dict[str, Wrestler]:
    wrestlers = [
        Wrestler("asha", "Asha Blaze", "Face", 48, 90),
        Wrestler("rohan", "Rohan Steel", "Heel", 52, 85),
        Wrestler("mina", "Mina Kage", "Heel", 44, 76),
        Wrestler("leo", "Leo Nova", "Face", 61, 70),
        Wrestler("jax", "Jax Thunder", "Face", 57, 82),
        Wrestler("ivy", "Ivy Wren", "Heel", 50, 66),
        Wrestler("ember", "Ember Vale", "Face", 55, 74),
        Wrestler("goro", "Goro Wolfe", "Heel", 63, 68),
    ]
    return {wrestler.id: wrestler for wrestler in wrestlers}
