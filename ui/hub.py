from __future__ import annotations

from typing import Dict, Optional

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Static

from domain.booking import is_valid_booking
from domain.models import Wrestler


class HubScreen(Screen):
    BINDINGS = [
        ("up", "focus_previous", "Up"),
        ("down", "focus_next", "Down"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Container(id="hub"):
            with Vertical(id="slots"):
                yield Button("Slot A: Empty", id="slot-a")
                yield Button("Slot B: Empty", id="slot-b")
                yield Static("Notes: —", id="notes")
            yield Button("Book Match", id="book")
        yield Footer()

    def on_mount(self) -> None:
        self.set_focus(self.query_one("#slot-a", Button))

    def update_view(
        self, roster: Dict[str, Wrestler], selected_a_id: Optional[str], selected_b_id: Optional[str]
    ) -> None:
        slot_a = roster[selected_a_id].name if selected_a_id else "Empty"
        slot_b = roster[selected_b_id].name if selected_b_id else "Empty"
        self.query_one("#slot-a", Button).label = f"Slot A: {slot_a}"
        self.query_one("#slot-b", Button).label = f"Slot B: {slot_b}"

        notes = "—"
        if selected_a_id and selected_b_id and selected_a_id != selected_b_id:
            wrestler_a = roster[selected_a_id]
            wrestler_b = roster[selected_b_id]
            if wrestler_a.alignment != wrestler_b.alignment:
                notes = "Face vs Heel bonus"
            else:
                notes = "Same alignment"
        self.query_one("#notes", Static).update(f"Notes: {notes}")

        book_button = self.query_one("#book", Button)
        book_button.disabled = not is_valid_booking(selected_a_id, selected_b_id)

    @on(Button.Pressed, "#slot-a")
    def _select_a(self) -> None:
        self.app.open_selector("A")

    @on(Button.Pressed, "#slot-b")
    def _select_b(self) -> None:
        self.app.open_selector("B")

    @on(Button.Pressed, "#book")
    def _book(self) -> None:
        self.app.open_confirm()
