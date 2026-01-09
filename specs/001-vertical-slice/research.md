# Research

## Decision: Load wrestler and match type data from JSON at startup

Rationale: The spec requires data-driven content and updates without code changes.

Alternatives considered: Hardcoded definitions in code; rejected because it violates data-driven requirements.

## Decision: Deterministic simulation using a seeded RNG in the sim layer

Rationale: Ensures repeatable outcomes for the same inputs and enables testing.

Alternatives considered: Non-seeded randomness; rejected due to non-determinism and testing gaps.

## Decision: Keyboard-only Textual UI flow with fixed screen sequence

Rationale: Matches the navigation contract and ensures usability in narrow terminals.

Alternatives considered: Mouse input or flexible navigation; rejected due to explicit constraints.
