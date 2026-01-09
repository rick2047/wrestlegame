<!--
Sync Impact Report:
Version change: template -> 1.0.0
Modified principles: placeholders -> Clean Code, Documentation, Testing, Tooling, Commits
Added sections: Technology & Tooling Requirements, Development Workflow & Quality Gates
Removed sections: none
Templates requiring updates:
- ✅ /home/droid/wrestlegame/.specify/templates/commands/plan.md
- ✅ /home/droid/wrestlegame/.specify/templates/commands/spec.md
- ✅ /home/droid/wrestlegame/.specify/templates/commands/tasks.md
- ✅ /home/droid/wrestlegame/.specify/templates/commands/README.md
- ✅ /home/droid/wrestlegame/.specify/templates/tasks-template.md
- ✅ /home/droid/wrestlegame/README.md
Follow-up TODOs:
- None.
-->
# WrestleGM Constitution

## Core Principles

### Clean Code And Single Purpose
Code MUST be readable, intentionally named, and organized into small single-purpose
units. Avoid duplication and keep business rules centralized. Prefer explicit logic
over cleverness, and keep functions and classes narrowly scoped.

### Documentation Always Updated
Any behavior change MUST update the relevant documentation in `docs/` and keep
MkDocs pages accurate. If no documentation changes are needed, the commit MUST
state why.

### Test-Heavy Development
All new behavior MUST include meaningful tests that cover core flows and edge
cases. Determinism and validation logic require dedicated tests. Use pytest and
keep tests maintainable.

### Python-Only Tooling
All production code MUST be Python. Dependencies are managed with `uv`, tests use
pytest, and documentation uses MkDocs. Avoid adding non-Python tooling unless
explicitly approved.

### Frequent Structured Commits
Work MUST be committed in small increments. Commit messages MUST have a short
header and a detailed explanation body.

## Technology & Tooling Requirements

- Python 3.10+ only for application code.
- `uv` is required for dependency management.
- pytest is required for test execution.
- MkDocs is required for documentation builds.

## Development Workflow & Quality Gates

- Every change MUST include appropriate tests and updated documentation.
- Deterministic simulation changes MUST include reproducibility tests.
- Changes that affect user flows MUST update `docs/` and `mkdocs` content.

## Governance

This constitution supersedes all other practices. Amendments MUST be documented,
versioned, and reviewed before adoption. Compliance MUST be checked during code
review. Commit messages MUST include a short header and a detailed body.

**Version**: 1.0.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-09
