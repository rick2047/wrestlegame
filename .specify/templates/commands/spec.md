# /speckit.spec Command Workflow

Purpose: Draft a feature specification in `specs/[###-feature]/spec.md`.

## Inputs
- User request and repo context
- Constitution: `.specify/memory/constitution.md`
- Requirements: `prd/main.md`

## Steps
1. Capture user scenarios as independently testable stories.
2. Define functional requirements with clear, testable language.
3. Specify edge cases and measurable success criteria.
4. Align constraints with the constitution (tooling, testing, documentation updates).

## Output
- Write `specs/[###-feature]/spec.md` using `.specify/templates/spec-template.md`.
- Ensure each story has acceptance scenarios and an independent test.

## Notes
- Use Python terminology where relevant.
- Avoid adding new dependencies unless required; prefer standard library.
- Keep language clear and accessible.
- If behavior changes, note documentation updates.
