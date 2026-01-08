# Command Templates

This directory documents how `/speckit.*` commands populate spec artifacts.

## Files
- `plan.md`: Generates the implementation plan from the feature spec.
- `spec.md`: Captures user stories, requirements, and success criteria.
- `tasks.md`: Produces implementation tasks grouped by user story.

## Usage Notes
- All outputs must comply with `.specify/memory/constitution.md`.
- Use Python + `uv` tooling and pytest for tests.
- Keep dependencies minimal; prefer the standard library.
- Document behavior changes in `docs/`.
