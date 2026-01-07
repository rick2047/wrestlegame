# Testing

## Framework
The project uses pytest.

## How to Run
```bash
uv run pytest
```

## What We Test
- **Determinism**: same seed produces same outcome.
- **Validation**: bookings require two distinct wrestlers.
- **Bounds**: popularity and stamina remain within 0–100.
- **Roster sanity**: IDs are unique.

## Adding Tests
- Place new tests in `tests/test_*.py`.
- Prefer small unit tests around `domain/` and `sim/`.
- Keep tests deterministic and avoid dependence on UI components.
