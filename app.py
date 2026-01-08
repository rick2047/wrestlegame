"""Textual application entry point and UI orchestration."""

from __future__ import annotations

from typing import Optional

from textual.app import App

from domain.booking import is_valid_booking
from domain.match_types import MatchType
from domain.models import Match
from domain.roster import seed_roster
from sim.engine import apply_result, simulate_match
from ui.confirm import ConfirmScreen
from ui.hub import HubScreen
from ui.match_type_selector import MatchTypeSelectorScreen
from ui.selector import SelectorScreen
from ui.simulating import SimulatingScreen
from ui.state import AppState


class WrestleGMApp(App):
    """Main Textual app that owns state and coordinates screen flow.

    Responsibilities:
    - Hold the live roster and the global AppState.
    - Route navigation between Hub, Selector, Confirm, Simulating, and Results screens.
    - Trigger simulations and apply stat deltas to the roster.
    """
    CSS_PATH = "ui/styles.tcss"
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self) -> None:
        """Initialize roster and application state."""
        super().__init__()
        self.roster = seed_roster()
        self.state = AppState()

    def on_mount(self) -> None:
        """Mount the hub screen and schedule the first refresh."""
        self.push_screen(HubScreen())
        self.call_after_refresh(self.refresh_hub)

    def refresh_hub(self) -> None:
        """Update the hub UI with current selections."""
        hub = self.screen
        if isinstance(hub, HubScreen):
            hub.update_view(
                self.roster,
                self.state.selected_a_id,
                self.state.selected_b_id,
                self.state.selected_match_type,
            )

    def open_selector(self, slot_label: str) -> None:
        """Open the selection modal for a slot, with opponent locking."""
        locked_id = (
            self.state.selected_b_id if slot_label == "A" else self.state.selected_a_id
        )

        def _on_selection(selected_id: Optional[str]) -> None:
            """Apply selection result and refresh the hub."""
            if selected_id:
                if slot_label == "A":
                    self.state.selected_a_id = selected_id
                else:
                    self.state.selected_b_id = selected_id
            self.refresh_hub()

        self.push_screen(
            SelectorScreen(self.roster, slot_label, locked_id, self.state.selected_match_type),
            _on_selection,
        )

    def open_confirm(self) -> None:
        """Open booking confirmation modal if selection is valid."""
        if not self.state.selected_match_type:
            self.notify("Select a match type before booking.", severity="warning")
            return
        if not is_valid_booking(
            self.state.selected_a_id,
            self.state.selected_b_id,
            self.state.selected_match_type,
        ):
            self.notify("Select two different wrestlers before booking.", severity="warning")
            return
        wrestler_a = self.roster[self.state.selected_a_id]
        wrestler_b = self.roster[self.state.selected_b_id]
        match_type = self.state.selected_match_type

        def _on_confirm(confirmed: bool) -> None:
            """Simulate the match if the user confirms."""
            if confirmed:
                self.book_match()

        self.push_screen(ConfirmScreen(wrestler_a, wrestler_b, match_type), _on_confirm)

    def book_match(self) -> None:
        """Simulate a booked match and transition to the results flow."""
        if not is_valid_booking(
            self.state.selected_a_id,
            self.state.selected_b_id,
            self.state.selected_match_type,
        ):
            return
        if self.state.selected_match_type is None:
            return
        match = Match(
            self.state.selected_a_id, self.state.selected_b_id, self.state.selected_match_type
        )
        # Simulation is pure; roster is mutated only by apply_result.
        result = simulate_match(match, self.roster, self.state.seed)
        apply_result(self.roster, result)
        self.state.last_match = match
        self.state.last_result = result
        self.state.seed += 1
        self.push_screen(SimulatingScreen(match, result))

    def reset_booking(self) -> None:
        """Clear the current booking and return to an empty hub state."""
        self.state.selected_a_id = None
        self.state.selected_b_id = None
        self.state.selected_match_type = None
        self.state.last_match = None
        self.state.last_result = None
        self.refresh_hub()

    def rematch(self) -> None:
        """Simulate a rematch using the last booked pairing."""
        if not self.state.last_match:
            return
        match = self.state.last_match
        result = simulate_match(match, self.roster, self.state.seed)
        apply_result(self.roster, result)
        self.state.last_result = result
        self.state.seed += 1
        self.push_screen(SimulatingScreen(match, result))

    def open_match_type(self) -> None:
        """Open the match type selection modal."""

        def _on_selection(selected_type: Optional[MatchType]) -> None:
            """Apply match type selection and refresh the hub."""
            if selected_type:
                self.state.selected_match_type = selected_type
            self.refresh_hub()

        self.push_screen(MatchTypeSelectorScreen(), _on_selection)


if __name__ == "__main__":
    WrestleGMApp().run()
