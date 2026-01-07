"""Wrestler selection modal screen."""

from __future__ import annotations

from typing import Dict, List, Optional

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Key
from textual.screen import ModalScreen
from textual.widgets import Label, ListItem, ListView, Static

from domain.models import Wrestler


class SelectorScreen(ModalScreen[Optional[str]]):
    """Modal for selecting a wrestler from the roster."""
    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("enter", "select", "Select"),
    ]

    def __init__(
        self,
        roster: Dict[str, Wrestler],
        slot_label: str,
        locked_id: Optional[str],
    ) -> None:
        super().__init__()
        self.roster = roster
        self.slot_label = slot_label
        self.locked_id = locked_id
        self._order: List[str] = []

    def compose(self) -> ComposeResult:
        """Compose the selector layout."""
        with Container(id="selector"):
            yield Label(f"Select Wrestler ({self.slot_label})", id="selector-title")
            yield ListView(id="roster-list")
            yield Static("", id="detail")
            with Horizontal(id="selector-actions"):
                yield Static("Enter: Select")
                yield Static("Esc: Cancel")

    def on_mount(self) -> None:
        """Populate roster list and set initial focus."""
        roster_list = self.query_one("#roster-list", ListView)
        for wrestler in self.roster.values():
            locked = " (locked)" if wrestler.id == self.locked_id else ""
            label = f"{wrestler.name} ({wrestler.alignment}){locked}"
            roster_list.append(ListItem(Label(label), id=wrestler.id))
            self._order.append(wrestler.id)
        self.set_focus(roster_list)
        self._update_detail()

    @on(ListView.Highlighted)
    def _on_highlighted(self, _: ListView.Highlighted) -> None:
        """Update detail panel when list selection changes."""
        self._update_detail()

    @on(ListView.Selected)
    def _on_selected(self, event: ListView.Selected) -> None:
        """Handle Enter selection from the list view."""
        wrestler_id = self._order[event.index]
        if wrestler_id == self.locked_id:
            self.notify("That wrestler is locked.", severity="warning")
            return
        self.dismiss(wrestler_id)

    def _update_detail(self) -> None:
        """Render stats for the currently highlighted wrestler."""
        roster_list = self.query_one("#roster-list", ListView)
        if roster_list.index is None:
            return
        wrestler_id = self._order[roster_list.index]
        wrestler = self.roster[wrestler_id]
        detail = (
            f"Alignment: {wrestler.alignment}\n"
            f"Popularity: {wrestler.popularity}\n"
            f"Stamina: {wrestler.stamina}"
        )
        self.query_one("#detail", Static).update(detail)

    def action_select(self) -> None:
        """Select the highlighted wrestler."""
        roster_list = self.query_one("#roster-list", ListView)
        if roster_list.index is None:
            return
        wrestler_id = self._order[roster_list.index]
        if wrestler_id == self.locked_id:
            self.notify("That wrestler is locked.", severity="warning")
            return
        self.dismiss(wrestler_id)

    def action_cancel(self) -> None:
        """Dismiss the modal without selection."""
        self.dismiss(None)

    def on_key(self, event: Key) -> None:
        """Handle fallback list navigation keys."""
        if event.key in {"k", "w"}:
            self.action_cursor_up()
            event.stop()
        elif event.key in {"j", "s"}:
            self.action_cursor_down()
            event.stop()
