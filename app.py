from __future__ import annotations

from typing import Optional

from textual.app import App

from domain.booking import is_valid_booking
from domain.models import Match
from domain.roster import seed_roster
from sim.engine import apply_result, simulate_match
from ui.confirm import ConfirmScreen
from ui.hub import HubScreen
from ui.selector import SelectorScreen
from ui.simulating import SimulatingScreen
from ui.state import AppState


class WrestleGMApp(App):
    CSS_PATH = "ui/styles.tcss"
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self) -> None:
        super().__init__()
        self.roster = seed_roster()
        self.state = AppState()

    def on_mount(self) -> None:
        self.push_screen(HubScreen())
        self.refresh_hub()

    def refresh_hub(self) -> None:
        hub = self.screen
        if isinstance(hub, HubScreen):
            hub.update_view(self.roster, self.state.selected_a_id, self.state.selected_b_id)

    def open_selector(self, slot_label: str) -> None:
        locked_id = (
            self.state.selected_b_id if slot_label == "A" else self.state.selected_a_id
        )

        def _on_selection(selected_id: Optional[str]) -> None:
            if selected_id:
                if slot_label == "A":
                    self.state.selected_a_id = selected_id
                else:
                    self.state.selected_b_id = selected_id
            self.refresh_hub()

        self.push_screen(SelectorScreen(self.roster, slot_label, locked_id), _on_selection)

    def open_confirm(self) -> None:
        if not is_valid_booking(self.state.selected_a_id, self.state.selected_b_id):
            self.notify("Select two different wrestlers before booking.", severity="warning")
            return
        wrestler_a = self.roster[self.state.selected_a_id]
        wrestler_b = self.roster[self.state.selected_b_id]

        def _on_confirm(confirmed: bool) -> None:
            if confirmed:
                self.book_match()

        self.push_screen(ConfirmScreen(wrestler_a, wrestler_b), _on_confirm)

    def book_match(self) -> None:
        if not is_valid_booking(self.state.selected_a_id, self.state.selected_b_id):
            return
        match = Match(self.state.selected_a_id, self.state.selected_b_id)
        result = simulate_match(match, self.roster, self.state.seed)
        apply_result(self.roster, result)
        self.state.last_match = match
        self.state.last_result = result
        self.state.seed += 1
        self.push_screen(SimulatingScreen(match, result))

    def reset_booking(self) -> None:
        self.state.selected_a_id = None
        self.state.selected_b_id = None
        self.state.last_match = None
        self.state.last_result = None
        self.refresh_hub()

    def rematch(self) -> None:
        if not self.state.last_match:
            return
        match = self.state.last_match
        result = simulate_match(match, self.roster, self.state.seed)
        apply_result(self.roster, result)
        self.state.last_result = result
        self.state.seed += 1
        self.push_screen(SimulatingScreen(match, result))


if __name__ == "__main__":
    WrestleGMApp().run()
