"""Match card hub screen."""

from __future__ import annotations

from typing import Dict, Optional

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.events import Key
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Static

from domain.booking import is_valid_booking
from domain.match_types import MatchTypeDefinition
from domain.models import Wrestler


class HubScreen(Screen):
    """Landing screen for slot selection and match booking.

    Provides two slots, a notes line for matchup context, and a booking action.
    """
    BINDINGS = [
        ("up", "focus_previous", "Up"),
        ("down", "focus_next", "Down"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the hub layout."""
        yield Header(show_clock=False)
        with Container(id="hub"):
            with Vertical(id="slots"):
                yield Button("Slot A: Empty", id="slot-a")
                yield Button("Slot B: Empty", id="slot-b")
                yield Button("Match Type: Unset", id="match-type")
                yield Static("Notes: —", id="notes")
            yield Button("Book Match", id="book")
        yield Footer()

    def on_mount(self) -> None:
        """Set initial focus to the first slot."""
        self.set_focus(self.query_one("#slot-a", Button))

    def action_focus_next(self) -> None:
        """Move focus to the next widget."""
        self.focus_next()

    def action_focus_previous(self) -> None:
        """Move focus to the previous widget."""
        self.focus_previous()

    def update_view(
        self,
        roster: Dict[str, Wrestler],
        selected_a_id: Optional[str],
        selected_b_id: Optional[str],
        match_types: Dict[str, MatchTypeDefinition],
        selected_match_type_id: Optional[str],
    ) -> None:
        """Update slot labels, notes, and booking button state."""
        slot_a = roster[selected_a_id].name if selected_a_id else "Empty"
        slot_b = roster[selected_b_id].name if selected_b_id else "Empty"
        self.query_one("#slot-a", Button).label = f"Slot A: {slot_a}"
        self.query_one("#slot-b", Button).label = f"Slot B: {slot_b}"
        match_type_label = "Unset"
        if selected_match_type_id and selected_match_type_id in match_types:
            match_type_label = match_types[selected_match_type_id].name
        self.query_one("#match-type", Button).label = f"Match Type: {match_type_label}"

        notes = "—"
        if selected_a_id and selected_b_id and selected_a_id != selected_b_id:
            wrestler_a = roster[selected_a_id]
            wrestler_b = roster[selected_b_id]
            if wrestler_a.alignment != wrestler_b.alignment:
                notes = "Face vs Heel bonus"
            else:
                notes = "Same alignment"
        if selected_match_type_id and selected_match_type_id in match_types:
            notes = f"{notes} | {match_types[selected_match_type_id].name}"
        self.query_one("#notes", Static).update(f"Notes: {notes}")

        book_button = self.query_one("#book", Button)
        book_button.disabled = not is_valid_booking(
            selected_a_id,
            selected_b_id,
            selected_match_type_id,
            set(match_types.keys()),
        )

    @on(Button.Pressed, "#slot-a")
    def _select_a(self) -> None:
        """Open selector for Slot A."""
        self.app.open_selector("A")

    @on(Button.Pressed, "#slot-b")
    def _select_b(self) -> None:
        """Open selector for Slot B."""
        self.app.open_selector("B")

    @on(Button.Pressed, "#book")
    def _book(self) -> None:
        """Open confirmation modal."""
        self.app.open_confirm()

    @on(Button.Pressed, "#match-type")
    def _select_match_type(self) -> None:
        """Open match type selector modal."""
        self.app.open_match_type()

    def on_key(self, event: Key) -> None:
        """Handle fallback focus navigation keys."""
        if event.key in {"k", "w"}:
            self.focus_previous()
            event.stop()
        elif event.key in {"j", "s"}:
            self.focus_next()
            event.stop()
