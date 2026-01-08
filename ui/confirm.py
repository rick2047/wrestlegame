"""Booking confirmation modal screen."""

from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Key
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static

from domain.match_types import MATCH_TYPE_LOOKUP, MatchType
from domain.models import Wrestler


class ConfirmScreen(ModalScreen[bool]):
    """Modal for confirming a booked match.

    Shows both wrestlers with key stats and returns True on confirm, False on back.
    """
    BINDINGS = [
        ("escape", "cancel", "Back"),
        ("left", "focus_previous", "Left"),
        ("right", "focus_next", "Right"),
    ]

    def __init__(self, wrestler_a: Wrestler, wrestler_b: Wrestler, match_type: MatchType) -> None:
        """Create the modal with selected wrestlers."""
        super().__init__()
        self.wrestler_a = wrestler_a
        self.wrestler_b = wrestler_b
        self.match_type = match_type

    def compose(self) -> ComposeResult:
        """Compose the confirmation layout."""
        match_label = MATCH_TYPE_LOOKUP[self.match_type].label
        a_proficient = "Yes" if self.wrestler_a.is_proficient(self.match_type) else "No"
        b_proficient = "Yes" if self.wrestler_b.is_proficient(self.match_type) else "No"
        with Container(id="confirm"):
            yield Label("Confirm Booking", id="confirm-title")
            yield Static(
                f"Match Type: {match_label}\n\n"
                f"{self.wrestler_a.name} ({self.wrestler_a.alignment})\n"
                f"Pop {self.wrestler_a.popularity}  Sta {self.wrestler_a.stamina}  Pro {a_proficient}\n"
                "vs\n"
                f"{self.wrestler_b.name} ({self.wrestler_b.alignment})\n"
                f"Pop {self.wrestler_b.popularity}  Sta {self.wrestler_b.stamina}  Pro {b_proficient}"
            )
            with Horizontal(id="confirm-actions"):
                yield Button("Confirm", id="confirm-yes")
                yield Button("Back", id="confirm-no")

    def on_mount(self) -> None:
        """Focus the confirm button by default."""
        self.set_focus(self.query_one("#confirm-yes", Button))

    def action_focus_next(self) -> None:
        """Move focus to the next widget."""
        self.focus_next()

    def action_focus_previous(self) -> None:
        """Move focus to the previous widget."""
        self.focus_previous()

    def on_key(self, event: Key) -> None:
        """Handle left/right fallback navigation keys."""
        if event.key in {"left", "left_arrow", "h", "a"}:
            self.focus_previous()
            event.stop()
        elif event.key in {"right", "right_arrow", "l", "d"}:
            self.focus_next()
            event.stop()

    @on(Button.Pressed, "#confirm-yes")
    def _on_confirm(self) -> None:
        """Dismiss with a True result."""
        self.dismiss(True)

    @on(Button.Pressed, "#confirm-no")
    def _on_back(self) -> None:
        """Dismiss with a False result."""
        self.dismiss(False)

    def action_cancel(self) -> None:
        """Treat cancel as a back action."""
        self.dismiss(False)
