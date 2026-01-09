# WrestleGM Vertical Slice

Prototype for booking and simulating a single match in a Textual TUI.

## Requirements
- Python 3.10+
- `uv`

## Setup
```bash
uv sync
```

## Run
```bash
uv run python app.py
```

## Tests
```bash
uv run pytest
```

## Design Docs
This repo includes a MkDocs-based design doc set in `docs/`.

```bash
uv run mkdocs serve
```

## Contribution Expectations
- Keep documentation in `docs/` updated for any behavior changes.
- Add tests for new behavior and edge cases (pytest).
- Use short commit headers with a detailed explanation body.
