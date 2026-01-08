# /speckit.tasks Command Workflow

Purpose: Generate `specs/[###-feature]/tasks.md` from design artifacts.

## Inputs
- `specs/[###-feature]/plan.md`
- `specs/[###-feature]/spec.md`
- `specs/[###-feature]/research.md`, `data-model.md`, `contracts/` (if present)
- Constitution: `.specify/memory/constitution.md`

## Steps
1. Group tasks by user story (US1, US2, ...), ordered by priority.
2. Add prerequisites and foundational work before story tasks.
3. Include tests for any sim/domain logic or validation changes.
4. Include documentation tasks for behavior changes.
5. Use concrete file paths that match the repo structure.

## Output
- Write `specs/[###-feature]/tasks.md` using `.specify/templates/tasks-template.md`.
- Remove all sample tasks and replace with real ones.

## Notes
- Tests use pytest and should be written to fail before implementation.
- Keep tasks small and single-purpose.
