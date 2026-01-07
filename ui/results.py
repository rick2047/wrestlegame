"""Results screen showing match outcome and actions."""

from __future__ import annotations

from typing import Dict, List

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.events import Key
from textual.screen import Screen
from textual.widgets import Button, Label, Static

from domain.models import Match, MatchResult, Wrestler


class ResultsScreen(Screen):
    """Screen for displaying winner, rating, and stat changes."""
    BINDINGS = [
        ("up", "focus_previous", "Up"),
        ("down", "focus_next", "Down"),
        ("escape", "back", "Back"),
    ]

    def __init__(self, match: Match, result: MatchResult) -> None:
        """Create the results screen for a specific match outcome."""
        super().__init__()
        self.match = match
        self.result = result

    def compose(self) -> ComposeResult:
        """Compose the results layout."""
        with Container(id="results"):
            yield Label("Match Result", id="results-title")
            yield Static("", id="results-summary")
            yield Static("", id="results-stats")
            with Vertical(id="results-actions"):
                yield Button("Book Another Match", id="results-reset")
                yield Button("Re-match", id="results-rematch")
                yield Button("Quit", id="results-quit")

    def on_mount(self) -> None:
        """Populate summary and stat changes after mount."""
        roster: Dict[str, Wrestler] = self.app.roster
        wrestler_a = roster[self.match.wrestler_a_id]
        wrestler_b = roster[self.match.wrestler_b_id]
        winner = wrestler_a if self.result.winner_id == wrestler_a.id else wrestler_b
        summary = f"Winner: {winner.name} ({winner.alignment})\nRating: {self.result.rating}/100"
        self.query_one("#results-summary", Static).update(summary)
        self.query_one("#results-stats", Static).update(
            _format_stats(wrestler_a, wrestler_b, self.result)
        )

    @on(Button.Pressed, "#results-reset")
    def _on_reset(self) -> None:
        """Clear booking and return to hub."""
        self.app.reset_booking()
        self.app.pop_screen()

    @on(Button.Pressed, "#results-rematch")
    def _on_rematch(self) -> None:
        """Run a rematch with the same pairing."""
        self.app.pop_screen()
        self.app.rematch()

    @on(Button.Pressed, "#results-quit")
    def _on_quit(self) -> None:
        """Exit the application."""
        self.app.exit()

    def action_back(self) -> None:
        """Return to the hub screen."""
        self.app.pop_screen()
        self.app.refresh_hub()

    def on_key(self, event: Key) -> None:
        """Handle fallback focus navigation keys."""
        if event.key in {"k", "w"}:
            self.focus_previous()
            event.stop()
        elif event.key in {"j", "s"}:
            self.focus_next()
            event.stop()


def _format_stats(wrestler_a: Wrestler, wrestler_b: Wrestler, result: MatchResult) -> str:
    """Return formatted before/after stat lines for both wrestlers."""
    lines: List[str] = ["Stat Changes"]
    for wrestler in (wrestler_a, wrestler_b):
        delta = result.deltas[wrestler.id]
        before_pop = wrestler.popularity - delta.popularity
        before_sta = wrestler.stamina - delta.stamina
        lines.append(
            f"{wrestler.name}\n"
            f"  Pop: {before_pop} -> {wrestler.popularity} ({delta.popularity:+d})\n"
            f"  Sta: {before_sta} -> {wrestler.stamina} ({delta.stamina:+d})"
        )
    return "\n".join(lines)
