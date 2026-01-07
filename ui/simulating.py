"""Simulating screen for pacing between booking and results."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Label, Static

from domain.models import Match, MatchResult
from ui.results import ResultsScreen


class SimulatingScreen(Screen):
    """Short-lived screen that auto-advances to results.

    Used as a pacing step between confirmation and results display.
    """
    def __init__(self, match: Match, result: MatchResult) -> None:
        """Create the simulating screen with the pending result."""
        super().__init__()
        self.match = match
        self.result = result

    def compose(self) -> ComposeResult:
        """Compose the simulating layout."""
        with Container(id="sim"):
            yield Label("Simulating match...", id="sim-title")
            yield Static("Please wait", id="sim-sub")

    def on_mount(self) -> None:
        """Schedule the transition to results."""
        self.set_timer(0.8, self._advance)

    def _advance(self) -> None:
        """Replace this screen with the results screen."""
        self.app.pop_screen()
        self.app.push_screen(ResultsScreen(self.match, self.result))
