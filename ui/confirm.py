from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static

from domain.models import Wrestler


class ConfirmScreen(ModalScreen[bool]):
    BINDINGS = [
        ("escape", "cancel", "Back"),
        ("left", "focus_previous", "Left"),
        ("right", "focus_next", "Right"),
    ]

    def __init__(self, wrestler_a: Wrestler, wrestler_b: Wrestler) -> None:
        super().__init__()
        self.wrestler_a = wrestler_a
        self.wrestler_b = wrestler_b

    def compose(self) -> ComposeResult:
        with Container(id="confirm"):
            yield Label("Confirm Booking", id="confirm-title")
            yield Static(
                f"{self.wrestler_a.name} ({self.wrestler_a.alignment})\n"
                f"Pop {self.wrestler_a.popularity}  Sta {self.wrestler_a.stamina}\n"
                "vs\n"
                f"{self.wrestler_b.name} ({self.wrestler_b.alignment})\n"
                f"Pop {self.wrestler_b.popularity}  Sta {self.wrestler_b.stamina}"
            )
            with Horizontal(id="confirm-actions"):
                yield Button("Confirm", id="confirm-yes")
                yield Button("Back", id="confirm-no")

    def on_mount(self) -> None:
        self.set_focus(self.query_one("#confirm-yes", Button))

    def action_focus_next(self) -> None:
        self._cycle_focus(1)

    def action_focus_previous(self) -> None:
        self._cycle_focus(-1)

    def _cycle_focus(self, direction: int) -> None:
        buttons = [
            self.query_one("#confirm-yes", Button),
            self.query_one("#confirm-no", Button),
        ]
        current = self.focused
        if current in buttons:
            index = buttons.index(current)
        else:
            index = 0
        buttons[(index + direction) % len(buttons)].focus()

    @on(Button.Pressed, "#confirm-yes")
    def _on_confirm(self) -> None:
        self.dismiss(True)

    @on(Button.Pressed, "#confirm-no")
    def _on_back(self) -> None:
        self.dismiss(False)

    def action_cancel(self) -> None:
        self.dismiss(False)
