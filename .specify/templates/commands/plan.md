# /speckit.plan Command Workflow

Purpose: Generate a feature plan in `specs/[###-feature]/plan.md` aligned with the
constitution and repo layout.

## Inputs
- Feature spec at `specs/[###-feature]/spec.md`
- Repo context: `AGENTS.md`, `prd/main.md`, `plan.md`, `docs/`
- Constitution: `.specify/memory/constitution.md`

## Steps
1. Read the feature spec and extract scope, constraints, and success criteria.
2. Confirm the project structure matches the repository (Python/Textual).
3. Draft the plan with:
   - Summary and technical context
   - Constitution check gates (names, single-purpose units, minimal deps, pytest)
   - Concrete structure decisions matching current repo layout
4. Note any open questions or missing details as TODOs.

## Constitution Gates (Must Pass)
- Names use domain language from `prd/main.md`; avoid abbreviations.
- Units are single-purpose; UI in `ui/`, sim in `sim/`, validation in `domain/`.
- No duplicated business rules; share logic via one module.
- Explicit validation and error paths at boundaries.
- Deterministic sim/domain logic with seeded RNG; tests required for changes.
- Python-only code; `uv` for deps; pytest for tests; MkDocs for docs.
- Documentation updates planned for any behavior changes.

## Output
- Write `specs/[###-feature]/plan.md` using `.specify/templates/plan-template.md`.
- Ensure placeholders are replaced and the constitution check is explicit.

## Notes
- Keep plan content concise and actionable.
- If required data is missing, mark with `TODO(...)`.
