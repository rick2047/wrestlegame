<!--
Sync Impact Report
- Version change: 0.2.0 -> 0.2.1
- Modified principles: Added VI. Standard Tooling and Minimal Dependencies; Added VII. Clear, Extensive Documentation
- Added sections: Tooling & Dependency Management
- Removed sections: None
- Templates requiring updates: ✅ .specify/templates/plan-template.md; ✅ .specify/templates/tasks-template.md; ✅ .specify/templates/spec-template.md (no changes needed); ✅ .specify/templates/commands/README.md; ✅ .specify/templates/commands/plan.md; ✅ .specify/templates/commands/spec.md; ✅ .specify/templates/commands/tasks.md; ✅ README.md (no changes needed); ✅ docs/testing.md (no changes needed)
- Follow-up TODOs: TODO(RATIFICATION_DATE): original adoption date unknown
-->
# WrestleGM Vertical Slice Constitution

## Core Principles

### I. Clear Names and Intent
- Names MUST reveal intent using domain terms from `prd/main.md` where applicable.
- Avoid abbreviations and overloaded terms; rename when behavior evolves.
- Public APIs, models, and UI labels MUST use consistent naming for the same concept.
Rationale: Clear naming reduces cognitive load and prevents semantic drift.

### II. Small, Single-Purpose Units
- Functions and classes MUST have one reason to change; split when they mix concerns.
- UI composition MUST stay in `ui/`; sim rules and RNG usage MUST stay in `sim/`.
- Domain validation MUST stay in `domain/` and remain UI-agnostic.
Rationale: Single-purpose units keep changes localized and make code easier to test.

### III. Single Source of Truth
- Business rules and validation logic MUST live in one place and be reused.
- Copy-pasted logic is not allowed; refactor into helpers or shared modules instead.
- Derived values MUST be computed consistently from the same inputs.
Rationale: A single source prevents divergence and subtle behavior differences.

### IV. Explicit Validation and Error Paths
- Validate inputs at boundaries (UI, sim entry points, and domain constructors).
- Errors MUST be explicit (exceptions or typed results) and contain actionable context.
- Silent failures and broad exception swallowing are not allowed.
Rationale: Clear error paths make defects diagnosable and safe to handle.

### V. Deterministic, Testable Logic
- Simulation and validation logic MUST be deterministic with the seeded RNG wrapper.
- Side effects (UI updates, IO) MUST be isolated from pure logic.
- Changes to `sim/` or `domain/` MUST include tests covering new or changed behavior.
Rationale: Determinism and tests keep outcomes stable and regressions visible.

### VI. Standard Tooling and Minimal Dependencies
- Code MUST be Python and use `uv` for dependency management.
- New dependencies MUST be justified and kept to the minimum required set.
- Tests MUST use pytest unless a specific exception is documented.
Rationale: Consistent tooling and small dependency graphs reduce friction and risk.

### VII. Clear, Extensive Documentation
- Documentation MUST be thorough enough to onboard a new contributor.
- Docs MUST prioritize clarity and plain language over completeness.
- Updates that change behavior MUST include matching documentation changes.
Rationale: Clear documentation preserves shared understanding over time.

## Module Boundaries & Dependencies

- `ui/` MAY depend on `domain/` and `sim/`, but MUST NOT embed rules.
- `sim/` MAY depend on `domain/` and MUST remain free of UI concerns.
- `domain/` MUST be pure data/validation with no UI or RNG dependencies.
- Cross-module imports MUST follow these directions and avoid cycles.

## Tooling & Dependency Management

- Use Python 3.10+ and manage dependencies with `uv`.
- Avoid adding dependencies without a clear, documented need and alternatives review.
- Prefer standard library solutions when they meet requirements.

## Development Workflow & Quality Gates

- Every change MUST keep code readable with meaningful names and focused units.
- For `sim/` and `domain/` changes, add/adjust tests and run `uv run pytest`,
  or document why tests were not run.
- Refactors MUST preserve behavior; if behavior changes, update docs and tests.
- Keep functions and modules small; when in doubt, split by responsibility.
- Commit frequently with short headers and detailed bodies explaining what changed
  and why.

## Governance

- This constitution supersedes all other development guidance.
- Amendments require an update to this file, a rationale, and a version bump
  following semantic versioning (MAJOR breaking, MINOR additive, PATCH clarifying).
- Reviews MUST include a constitution compliance check and note any exceptions.
- Use `AGENTS.md` and `prd/main.md` for runtime development guidance.

**Version**: 0.2.1 | **Ratified**: TODO(RATIFICATION_DATE): original adoption date unknown | **Last Amended**: 2026-01-08
