"""Match type selection modal screen."""

from __future__ import annotations

from typing import List, Optional

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Key
from textual.screen import ModalScreen
from textual.widgets import Label, ListItem, ListView, Static

from domain.match_types import MatchTypeDefinition


class MatchTypeSelectorScreen(ModalScreen[Optional[str]]):
    """Modal for selecting a match type."""

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("enter", "select", "Select"),
    ]

    def __init__(self, match_types: List[MatchTypeDefinition]) -> None:
        """Create the match type selector."""
        super().__init__()
        self.match_types = match_types
        self._order: List[str] = []

    def compose(self) -> ComposeResult:
        """Compose the match type selector layout."""
        with Container(id="match-type-selector"):
            yield Label("Select Match Type", id="match-type-title")
            yield ListView(id="match-type-list")
            with Horizontal(id="match-type-actions"):
                yield Static("Enter: Select")
                yield Static("Esc: Cancel")

    def on_mount(self) -> None:
        """Populate match type list and set initial focus."""
        match_type_list = self.query_one("#match-type-list", ListView)
        for match_type in self.match_types:
            match_type_list.append(ListItem(Label(match_type.name), id=match_type.id))
            self._order.append(match_type.id)
        self.set_focus(match_type_list)

    def action_focus_next(self) -> None:
        """Move focus to the next widget."""
        self.focus_next()

    def action_focus_previous(self) -> None:
        """Move focus to the previous widget."""
        self.focus_previous()

    @on(ListView.Selected)
    def _on_selected(self, event: ListView.Selected) -> None:
        """Handle Enter selection from the list view."""
        match_type = self._order[event.index]
        self.dismiss(match_type)

    def action_select(self) -> None:
        """Select the highlighted match type."""
        match_type_list = self.query_one("#match-type-list", ListView)
        if match_type_list.index is None:
            return
        match_type = self._order[match_type_list.index]
        self.dismiss(match_type)

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
