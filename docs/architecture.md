# Architecture

## High-Level Overview
The prototype is divided into three layers:
- **Domain** (`domain/`): plain data models and booking validation.
- **Simulation** (`sim/`): deterministic RNG and match resolution logic.
- **UI** (`ui/`): Textual screens, styles, and shared app state.

The goal is to keep simulation logic pure and testable, while the UI layer focuses on user flow and presentation.

## Data Flow
1. **Selection**: the user selects Wrestler A, Wrestler B, and match type.
2. **Confirmation**: the booking summary is shown with match type and proficiency.
3. **Simulation**: `simulate_match` computes winner, rating, and stat deltas.
4. **Apply**: `apply_result` mutates the roster with clamped stats.
5. **Results**: the UI shows winner, match type, rating, and before/after stats.

## Modules and Responsibilities
- `app.py`
  - Owns the Textual `App`, global roster, and `AppState`.
  - Orchestrates navigation between screens.
- `domain/models.py`
  - `Wrestler`, `Match`, `MatchResult`, `StatDelta`.
  - `clamp_stat` for 0–100 bounds.
- `domain/match_types.py`
  - `MatchType` list and tuning data.
- `domain/roster.py`
  - `seed_roster()` returns a small, hard-coded roster.
- `domain/booking.py`
  - `is_valid_booking()` validates slot selection state.
- `sim/rng.py`
  - `RNG` wrapper for deterministic randomness.
- `sim/engine.py`
  - `simulate_match()` and `apply_result()`.
- `ui/state.py`
  - `AppState` for current selections and last result.
- `ui/*`
  - Screens for Hub, Selector, Match Type Selector, Confirm, Simulating, Results.
  - `ui/styles.tcss` for layout and basic presentation.

## Extensibility Notes
- To add new screens, follow the pattern in `ui/` and wire in `app.py`.
- To add new stats, extend `Wrestler` and update sim rules and UI display.
- To introduce persistence, add a storage layer that serializes `roster` and `AppState`.
