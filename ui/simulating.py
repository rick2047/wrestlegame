from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Label, Static

from domain.models import Match, MatchResult
from ui.results import ResultsScreen


class SimulatingScreen(Screen):
    def __init__(self, match: Match, result: MatchResult) -> None:
        super().__init__()
        self.match = match
        self.result = result

    def compose(self) -> ComposeResult:
        with Container(id="sim"):
            yield Label("Simulating match...", id="sim-title")
            yield Static("Please wait", id="sim-sub")

    def on_mount(self) -> None:
        self.set_timer(0.8, self._advance)

    def _advance(self) -> None:
        self.app.pop_screen()
        self.app.push_screen(ResultsScreen(self.match, self.result))
