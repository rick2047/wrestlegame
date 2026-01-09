# Implementation Plan: WrestleGM Vertical Slice Match Flow

**Branch**: `001-vertical-slice` | **Date**: 2026-01-09 | **Spec**: /home/droid/wrestlegame/specs/001-vertical-slice/spec.md  
**Input**: Feature specification from `/specs/001-vertical-slice/spec.md`

## Summary

Deliver the end-to-end single-match booking flow in the Textual TUI, with data-driven match types and deterministic simulation, while keeping UI, domain, and simulation layers cleanly separated.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: Textual, uv  
**Storage**: JSON configuration files in `data/` (wrestlers, match types)  
**Testing**: pytest  
**Target Platform**: Local terminal  
**Project Type**: single  
**Performance Goals**: Interactive actions respond within 200ms on a local machine  
**Constraints**: Keyboard-only navigation, deterministic simulation with seeded RNG  
**Scale/Scope**: Single-match flow, small default roster and match type set

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Names use domain language from `prd/main.md`; avoid abbreviations: PASS
- Units are single-purpose; UI in `ui/`, sim in `sim/`, validation in `domain/`: PASS
- No duplicated business rules; share logic via one module: PASS
- Explicit validation and error paths at boundaries: PASS
- Deterministic sim/domain logic with seeded RNG; tests required for changes: PASS
- Python-only code; `uv` for deps; pytest for tests; MkDocs for docs: PASS
- Documentation updates planned for any behavior changes: PASS

## Project Structure

### Documentation (this feature)

```text
specs/001-vertical-slice/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
app.py

domain/
├── __init__.py
├── models.py
├── booking.py
├── match_types.py
└── roster.py

sim/
├── __init__.py
├── rng.py
└── engine.py

ui/
├── __init__.py
├── confirm.py
├── hub.py
├── match_type_selector.py
├── results.py
├── selector.py
├── simulating.py
├── state.py
└── styles.tcss

tests/
└── test_*.py
```

**Structure Decision**: Single project using existing `domain/`, `sim/`, and `ui/` packages with `app.py` as the Textual entry point.

## Phase Plan

### Phase 0: Outline & Research

- Produce `research.md` with decisions for data-driven configs, deterministic simulation, and keyboard-first UI flow.

### Phase 1: Design & Contracts

- Produce `data-model.md` covering entities, relationships, and validation rules.
- Produce OpenAPI contracts in `contracts/` representing data loading and simulation boundaries.
- Produce `quickstart.md` with run/test steps.
- Update agent context via `.specify/scripts/bash/update-agent-context.sh codex`.
- Re-check constitution gates post-design.

## Constitution Check (Post-Design)

- Names use domain language from `prd/main.md`; avoid abbreviations: PASS
- Units are single-purpose; UI in `ui/`, sim in `sim/`, validation in `domain/`: PASS
- No duplicated business rules; share logic via one module: PASS
- Explicit validation and error paths at boundaries: PASS
- Deterministic sim/domain logic with seeded RNG; tests required for changes: PASS
- Python-only code; `uv` for deps; pytest for tests; MkDocs for docs: PASS
- Documentation updates planned for any behavior changes: PASS

## Complexity Tracking

> No violations to justify.
