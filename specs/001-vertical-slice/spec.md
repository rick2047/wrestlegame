# Feature Specification: WrestleGM Vertical Slice Match Flow

**Feature Branch**: `001-vertical-slice`  
**Created**: 2026-01-09  
**Status**: Draft  
**Input**: User description: "read prd1.md and implement features as shown in it"

## Clarifications

### Session 2026-01-09

- Q: If wrestler or match type data is missing/empty at startup, what should the app do? → A: Load a small built-in fallback dataset.
- Q: Should the system allow booking the same wrestler in both slots? → A: Block booking if both slots are the same wrestler.
- Q: How should the system handle stat deltas that exceed 0–100 bounds? → A: Clamp popularity and stamina to 0–100 after applying deltas.
- Q: If the user cancels a modal, should the selection be cleared? → A: Keep the previous selection (if any).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Book And Simulate A Match (Priority: P1)

As a player, I want to book a single match end-to-end so I can see a deterministic result and ratings from my chosen roster.

**Why this priority**: This is the core vertical slice loop and defines whether the product is usable at all.

**Independent Test**: Can be fully tested by booking a valid match with any two wrestlers and any match type, confirming it, and receiving a result screen with deltas.

**UI Reference**: Appendix - Match Card Hub, Confirm Booking Modal, Simulating Screen, Results Screen.

**Acceptance Scenarios**:

1. **Given** the match hub is open with valid Slot A, Slot B, and Match Type selections, **When** I confirm booking, **Then** the app runs the simulation and shows a results screen.
2. **Given** I provide the same inputs and seed twice, **When** I run the simulation, **Then** the winner, rating, and deltas match exactly.

---

### User Story 2 - Select Wrestlers With Clear Feedback (Priority: P2)

As a player, I want to select wrestlers for each slot and view their key stats so I can make informed booking decisions.

**Why this priority**: Selecting participants is required to book a match, and the preview reduces guesswork.

**Independent Test**: Can be fully tested by opening the selection list, choosing a wrestler, and verifying the selection and preview behavior.

**UI Reference**: Appendix - Wrestler Selection Modal.

**Acceptance Scenarios**:

1. **Given** the wrestler list is open, **When** I move the selection, **Then** the preview updates to show the highlighted wrestler's popularity, stamina, and alignment.
2. **Given** one slot is already filled, **When** I open the other slot's list, **Then** the already-selected wrestler is disabled and cannot be chosen.

---

### User Story 3 - Choose Match Types That Affect Outcomes (Priority: P3)

As a player, I want to choose a match type and have it change ratings and stat deltas so match styles feel distinct.

**Why this priority**: Match types are a key differentiator and must be data-driven to enable future content.

**Independent Test**: Can be fully tested by selecting two different match types for the same wrestlers and verifying that the results reflect the configured modifiers.

**UI Reference**: Appendix - Match Type Selection Modal.

**Acceptance Scenarios**:

1. **Given** multiple match types exist, **When** I select a different match type, **Then** the match hub reflects the new type before booking.
2. **Given** the same wrestlers and seed, **When** I simulate two different match types, **Then** the rating and deltas reflect the configured modifiers for each type.

---

### Edge Cases

- What happens when no wrestlers or match types are available at startup (fallback roster/match types should load)?
- How does the system prevent booking when Slot A and Slot B are the same wrestler (booking must be blocked)?
- What happens when stat changes would push popularity or stamina below 0 or above 100 (clamp to 0–100 after applying deltas)?
- How does the UI behave when a selection modal is cancelled (keep prior selection if present)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST load wrestler and match type definitions from external configuration at startup.
- **FR-001a**: If external wrestler or match type data is missing or empty at startup, system MUST load a built-in fallback dataset with at least 2 wrestlers and 1 match type.
- **FR-002**: System MUST allow selection of two distinct wrestlers and one match type before booking.
- **FR-002a**: System MUST block booking when Slot A and Slot B are the same wrestler.
- **FR-003**: System MUST disable booking until Slot A, Slot B, and Match Type are valid.
- **FR-003a**: System MUST retain prior selections when a selection modal is cancelled.
- **FR-004**: System MUST provide a wrestler selection modal with a list and a live stat preview.
- **FR-005**: System MUST provide a match type selection modal with a selectable list.
- **FR-006**: System MUST provide a confirmation step that summarizes the chosen wrestlers and match type and does not allow edits.
- **FR-007**: System MUST simulate matches deterministically based on a provided seed and the selected inputs.
- **FR-008**: System MUST apply match type modifiers additively to ratings and stat deltas.
- **FR-009**: System MUST return results that include match type identity and applied modifiers for auditing.
- **FR-010**: System MUST show a results screen with winner, rating, and popularity/stamina deltas.
- **FR-011**: System MUST support rematch (preserve selections) and new match (reset selections).
- **FR-012**: System MUST enforce keyboard-only navigation with a single active focus context.
- **FR-013**: System MUST clamp popularity and stamina to 0–100 after applying deltas.
- **FR-014**: System MUST complete the required flow without dead ends: hub, selection, type, confirm, simulate, results.

### Key Entities *(include if feature involves data)*

- **WrestlerDefinition**: A roster entry with identity, name, alignment, popularity, and stamina used for booking and simulation.
- **MatchTypeDefinition**: A match style with identity, name, optional description, and modifiers that influence outcomes.
- **Match**: A booking that references two wrestlers and a match type.
- **MatchResult**: The immutable outcome including winner, rating, deltas, match type identity, and applied modifiers.
- **AppState**: The single source of truth for selections, seed, and last result.

## Assumptions

- A small default roster and a small default set of match types are available at startup, with a fallback of at least 2 wrestlers and 1 match type.
- The seed is provided before booking begins and remains constant for a single simulated match.
- The vertical slice only covers single-match booking and simulation; multi-match cards remain out of scope.

## Dependencies

- Wrestler and match type data are available in external configuration before the app starts.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can complete the full book-confirm-simulate-results loop in under 60 seconds without external help.
- **SC-002**: Repeating a match with the same inputs and seed yields identical winner, rating, and deltas 100% of the time.
- **SC-003**: In a 100-match test set, no popularity or stamina value falls below 0 or exceeds 100 after deltas are applied.
- **SC-004**: 100% of interactive controls are reachable and operable using only keyboard inputs.

## Appendix: ASCII UI Mockups (Reference)

### Match Card Hub

```text
┌────────────────────────────┐
│ MATCH CARD                 │
├────────────────────────────┤
│ Slot A: [ Empty ]          │
│ Slot B: [ Empty ]          │
│ Type : Singles             │
│                            │
│ [ Book Match ]             │
└────────────────────────────┘
```

### Wrestler Selection Modal

```text
┌────────────────────────────┐
│ SELECT WRESTLER            │
├────────────────────────────┤
│ > John Steel               │
│   Max Power                │
│   Night Fang               │
│                            │
│ Pop: 72  Sta: 65  Face     │
└────────────────────────────┘
```

### Match Type Selection Modal

```text
┌────────────────────────────┐
│ SELECT MATCH TYPE          │
├────────────────────────────┤
│ > Singles                  │
│   No DQ                    │
│   Hardcore                 │
└────────────────────────────┘
```

### Confirm Booking Modal

```text
┌────────────────────────────┐
│ CONFIRM MATCH              │
├────────────────────────────┤
│ John Steel vs Max Power    │
│ Type: Singles              │
│                            │
│ [ Confirm ]   [ Back ]     │
└────────────────────────────┘
```

### Simulating Screen

```text
┌────────────────────────────┐
│ SIMULATING MATCH...        │
│                            │
│ Please wait                │
└────────────────────────────┘
```

### Results Screen

```text
┌────────────────────────────┐
│ MATCH RESULT               │
├────────────────────────────┤
│ Type : Singles             │
│ Winner: John Steel         │
│ Rating: ★★★★☆             │
│                            │
│ Pop: +5 / -3               │
│ Sta: -10 / -10             │
│                            │
│ [ Rematch ] [ New ] [ Quit ]
└────────────────────────────┘
```
