"""Tests for booking flow orchestration without UI loop."""

from __future__ import annotations

from typing import List

from app import WrestleGMApp
from ui.simulating import SimulatingScreen


class AppHarness(WrestleGMApp):
    """Test-friendly app that captures screen pushes and notifications."""

    def __init__(self) -> None:
        super().__init__()
        self.pushed: List[object] = []
        self.notices: List[str] = []

    def push_screen(self, screen, *args, **kwargs):  # type: ignore[override]
        self.pushed.append(screen)
        return None

    def notify(self, message: str, **kwargs):  # type: ignore[override]
        self.notices.append(message)
        return None


def test_book_match_sets_result_and_pushes_screen() -> None:
    """Booking should set match/result state and push simulating screen."""
    app = AppHarness()
    app.state.selected_a_id = "john_steel"
    app.state.selected_b_id = "max_power"
    app.state.selected_match_type_id = "singles"

    app.book_match()

    assert app.state.last_match is not None
    assert app.state.last_result is not None
    assert app.pushed
    assert isinstance(app.pushed[-1], SimulatingScreen)
    assert app.state.last_result.match_type_id == "singles"
    assert app.state.last_result.match_type_name == "Singles"
    assert app.state.last_result.applied_modifiers


def test_open_confirm_requires_match_type() -> None:
    """Confirm should warn if match type is missing."""
    app = AppHarness()
    app.state.selected_a_id = "john_steel"
    app.state.selected_b_id = "max_power"

    app.open_confirm()

    assert app.notices
    assert "match type" in app.notices[-1].lower()
