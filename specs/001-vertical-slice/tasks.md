---

description: "Task list for WrestleGM Vertical Slice Match Flow"
---

# Tasks: WrestleGM Vertical Slice Match Flow

**Input**: Design documents from `/specs/001-vertical-slice/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Required by the constitution; include tests for new behavior and validation changes.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 [P] Create data configuration files in `data/wrestlers.json` and `data/match_types.json`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 [P] Add determinism tests for match results in `tests/test_determinism.py`
- [X] T003 [P] Add bounds clamping tests for popularity/stamina in `tests/test_bounds.py`
- [X] T004 [P] Add match type modifier/audit tests in `tests/test_match_type_modifiers.py`
- [X] T005 [P] Add fallback dataset loading tests in `tests/test_roster_loading.py`
- [X] T006 [P] Add booking validation tests for distinct wrestlers in `tests/test_booking.py`
- [X] T007 [P] Update domain entities for data-driven definitions and match results in `domain/models.py`
- [X] T008 [P] Replace hardcoded match types with JSON loading and lookup helpers in `domain/match_types.py`
- [X] T009 [P] Replace hardcoded roster seeding and add fallback dataset loading in `domain/roster.py`
- [X] T010 [P] Expand booking validation to enforce distinct wrestlers and valid match type IDs in `domain/booking.py`
- [X] T011 Update simulation inputs/results to apply match type modifiers and include audit fields in `sim/engine.py`
- [X] T012 Update shared UI state to track match type IDs and match results with modifiers in `ui/state.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Book And Simulate A Match (Priority: P1) 🎯 MVP

**Goal**: Enable booking, confirmation, simulation, and results for a single match.

**Independent Test**: Book any valid match from the hub, confirm, and see a results screen with winner, rating, and deltas.

### Tests for User Story 1

- [X] T013 [P] [US1] Add booking flow tests for confirm/simulate/results in `tests/test_ui_flow.py`

### Implementation for User Story 1

- [X] T014 [US1] Update match hub controls, disabled state, and navigation flow in `ui/hub.py`
- [X] T015 [US1] Render confirmation summary and confirm/back actions in `ui/confirm.py`
- [X] T016 [US1] Implement non-interactive simulating screen with auto-advance in `ui/simulating.py`
- [X] T017 [US1] Render results summary, rematch, new match, and quit actions in `ui/results.py`
- [X] T018 [US1] Orchestrate screen flow and apply stat deltas in the UI layer via `app.py`

**Checkpoint**: User Story 1 is fully functional and independently testable

---

## Phase 4: User Story 2 - Select Wrestlers With Clear Feedback (Priority: P2)

**Goal**: Allow wrestler selection with stat preview and locked opponent handling.

**Independent Test**: Open selection for each slot, view live preview updates, and confirm the locked wrestler cannot be selected.

### Tests for User Story 2

- [X] T019 [P] [US2] Add selector preview, locked choice, and cancel-retain tests in `tests/test_selector.py`

### Implementation for User Story 2

- [X] T020 [US2] Update wrestler list rendering, preview panel, locked state, and cancel retention in `ui/selector.py`
- [X] T021 [US2] Wire slot selection handlers and locked opponent passing in `ui/hub.py`

**Checkpoint**: User Story 2 is fully functional and independently testable

---

## Phase 5: User Story 3 - Choose Match Types That Affect Outcomes (Priority: P3)

**Goal**: Allow match type selection and ensure match modifiers influence results.

**Independent Test**: Select a different match type and verify the hub and results reflect the chosen type and modifiers.

### Tests for User Story 3

- [X] T022 [P] [US3] Add match type selection tests in `tests/test_match_types.py`

### Implementation for User Story 3

- [X] T023 [US3] Render match type selection list and selection handling in `ui/match_type_selector.py`
- [X] T024 [US3] Wire match type selection modal and display in `ui/hub.py`

**Checkpoint**: User Story 3 is fully functional and independently testable

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T025 [P] Add keyboard navigation coverage tests in `tests/test_keyboard_navigation.py`
- [X] T026 [P] Enforce keyboard-only focus rules in `ui/hub.py`, `ui/selector.py`, `ui/match_type_selector.py`, `ui/confirm.py`, `ui/results.py`
- [X] T027 [P] Remove 40-column constraint from `ui/styles.tcss`
- [X] T028 [P] Add manual validation checklist for SC-001 and SC-004 in `docs/testing.md`
- [X] T029 [P] Update UI flow documentation in `docs/ui-flow.md`
- [X] T030 [P] Update simulation documentation for match type modifiers and audit fields in `docs/simulation.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: Depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - no dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - independent but integrates with hub state
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - independent but integrates with hub state

### Parallel Opportunities

- Setup and Foundational tasks marked [P] can run in parallel
- After Foundational, User Stories 1-3 can proceed in parallel if staffed
- Polish tasks can run in parallel after user story completion

---

## Parallel Example: User Story 1

```bash
Task: "Update match hub controls, disabled state, and navigation flow in ui/hub.py"
Task: "Render confirmation summary and confirm/back actions in ui/confirm.py"
Task: "Implement non-interactive simulating screen with auto-advance in ui/simulating.py"
```

---

## Parallel Example: User Story 2

```bash
Task: "Update wrestler list rendering, preview panel, and locked state behavior in ui/selector.py"
Task: "Wire slot selection handlers and locked opponent passing in ui/hub.py"
```

---

## Parallel Example: User Story 3

```bash
Task: "Render match type selection list and selection handling in ui/match_type_selector.py"
Task: "Wire match type selection modal and display in ui/hub.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate User Story 1 independently

### Incremental Delivery

1. Setup + Foundational
2. User Story 1 → validate
3. User Story 2 → validate
4. User Story 3 → validate

---

## Notes

- [P] tasks = different files, no dependencies
- Each user story should be independently completable and testable
- Keep UI, domain, and sim boundaries intact per plan.md
