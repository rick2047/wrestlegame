# WrestleGM Design Docs

This documentation describes the vertical slice prototype for booking and simulating a single match in a Textual TUI. It explains the domain model, simulation rules, UI flow, and testing approach so new contributors can ramp up quickly.

## Goals
- Provide a playable end-to-end loop: select A/B, confirm booking, simulate, and show results.
- Keep simulation deterministic under a fixed seed for reproducibility and tests.
- Ensure the TUI is navigable without a mouse.

## Non-Goals
- Multi-match cards, weeks/seasons, economy, or storylines.
- Persistence or save/load.
- AI booking or outcome explanations.

## Quick Start
```bash
uv sync
uv run python app.py
```

## Where to Look First
- `app.py`: app entry point and high-level UI flow wiring.
- `domain/`: data model, roster seed, booking validation.
- `sim/`: deterministic RNG and match simulation logic.
- `ui/`: Textual screens and styles.
- `tests/`: simulation and validation tests.
- `docs/api/`: API reference generated from docstrings.

## Key Design Principles
- Pure simulation logic: no UI state or side effects in the simulation layer.
- Single source of truth for UI state: selection, last match, seed, and results.
- Input-first UX: all screens respond to keyboard navigation.
