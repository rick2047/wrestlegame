# Repository Guidelines

## Project Structure & Module Organization
This repo is a Python/Textual prototype for the WrestleGM vertical slice.

- `app.py`: Textual app entry point.
- `domain/`: data models, booking validation, and roster seed data.
- `sim/`: deterministic simulation engine and RNG wrapper.
- `ui/`: Textual screens, styles, and shared UI state.
- `plan.md`: implementation plan for the vertical slice.
- `prd/main.md`: product requirements guide.
- `tests/`: pytest suite for simulation and validation.

Keep new modules small and focused; group UI by screen and keep sim logic pure.

## Build, Test, and Development Commands
- `uv run python app.py`: run the Textual TUI prototype in the uv venv.
- `uv run pytest`: run the test suite in the uv venv.

No build step is required for the current prototype.

## Coding Style & Naming Conventions
- Python style: PEP 8, 4-space indentation, and type hints where practical.
- Naming: `snake_case` for functions/variables, `PascalCase` for classes, and `UPPER_SNAKE_CASE` for constants.
- Keep code ASCII-only unless a file already uses Unicode characters.

## Testing Guidelines
- Framework: pytest.
- Location: `tests/` directory, with files named `test_*.py`.
- Focus: determinism (seeded RNG), bounds checking (0–100), and validation of booking rules.
- Default expectation: run `uv run pytest` before reporting changes.

## Commit & Pull Request Guidelines
- Commit messages must include a concise header and a detailed explanation body.
- PRs should include: a concise summary, testing notes (commands run), and any UX notes or screenshots if UI changes are made.

## Configuration & Data Notes
- Use `uv sync` after dependency changes to refresh `.venv` and `uv.lock`.
- The RNG seed is entered at startup; use a fixed seed for deterministic behavior during testing.

## Active Technologies
- Python 3.10+ + Textual (UI), pytest (tests), uv (env/deps) (001-extract-prd-specs)
- N/A (documentation-only outputs) (001-extract-prd-specs)
- Python 3.10+ + Textual, uv (001-vertical-slice)
- JSON configuration files in `data/` (wrestlers, match types) (001-vertical-slice)

## Recent Changes
- 001-extract-prd-specs: Added Python 3.10+ + Textual (UI), pytest (tests), uv (env/deps)
