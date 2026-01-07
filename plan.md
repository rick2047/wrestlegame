# WrestleGM – Vertical Slice Implementation Plan (Jira‑Style)

This document expands the Vertical Slice plan into **feature‑based Jira epics and stories**, with clear acceptance criteria and implementation notes.  
Scope is **strictly the vertical slice**: booking and simulating **one match** in a Textual (TUI) application.

---

# EPIC 0 – Project & Technical Foundation

## Story 0.1 – Project bootstrap & tooling
**Description**  
Set up the repository, environment, and baseline tooling so development can proceed consistently.

**Tasks**
- Initialize Python project using `uv`
- Add `pyproject.toml`
- Add dependencies: `textual`, `pytest`
- Add basic README with run instructions

**Acceptance Criteria**
- `uv run python app.py` launches a placeholder Textual app
- `pytest` runs successfully (even if empty)

---

## Story 0.2 – Repository structure
**Description**  
Create a clean, modular folder structure separating UI, domain, and simulation logic.

**Tasks**
- Create `ui/`, `domain/`, `tests/` folders
- Add empty module files as placeholders

**Acceptance Criteria**
- Imports resolve cleanly
- No circular dependencies

---

# EPIC 1 – Domain Model & Roster

## Story 1.1 – Wrestler data model
**Description**  
Define the Wrestler entity used across UI and simulation.

**Fields**
- `id: str`
- `name: str`
- `alignment: Literal["Face","Heel"]`
- `popularity: int (0–100)`
- `stamina: int (0–100)`

**Acceptance Criteria**
- Wrestler is a dataclass
- Validation ensures popularity and stamina are clamped

---

## Story 1.2 – Match & MatchResult models
**Description**  
Create models representing a booked match and its outcome.

**Match**
- wrestler_a_id
- wrestler_b_id

**MatchResult**
- winner_id
- loser_id
- rating
- stat_deltas (popularity & stamina per wrestler)

**Acceptance Criteria**
- Models are immutable once created
- MatchResult contains only computed values (no UI state)

---

## Story 1.3 – Seed roster
**Description**  
Provide a small, hardcoded roster for the slice.

**Tasks**
- Add 4–10 wrestlers
- Ensure mix of Faces and Heels

**Acceptance Criteria**
- Roster loads at app start
- IDs are unique and stable

---

# EPIC 2 – Simulation Engine

## Story 2.1 – Deterministic RNG wrapper
**Description**  
Ensure all randomness is seed‑controlled.

**Tasks**
- Create RNG wrapper class
- Accept seed explicitly

**Acceptance Criteria**
- Same seed produces identical random streams

---

## Story 2.2 – Winner calculation
**Description**  
Determine the match winner using weighted stats.

**Logic**
- Weight = popularity + stamina + small random factor

**Acceptance Criteria**
- Higher stats win more often
- Upsets remain possible
- Deterministic under fixed seed

---

## Story 2.3 – Match rating calculation
**Description**  
Calculate a match rating.

**Logic**
- Base = average popularity
- + Face vs Heel bonus
- − low stamina penalty
- ± small random variance

**Acceptance Criteria**
- Rating always within defined bounds
- Deterministic with seed

---

## Story 2.4 – Stat delta calculation
**Description**  
Apply stat changes after match.

**Rules**
- Winner popularity +X
- Loser popularity −Y or 0
- Both stamina −Z

**Acceptance Criteria**
- Stats never exceed 0–100
- Deltas are explicit in MatchResult

---

## Story 2.5 – Simulation engine orchestration
**Description**  
Combine winner, rating, and deltas into one function.

**Function**
`simulate_match(match, roster, seed) -> MatchResult`

**Acceptance Criteria**
- No side effects
- UI applies deltas separately

---

# EPIC 3 – Core App State & Navigation

## Story 3.1 – Global app state
**Description**  
Create a single source of truth for UI flow.

**State**
- selected_a_id
- selected_b_id
- last_result
- seed

**Acceptance Criteria**
- State survives screen transitions
- State resets correctly

---

## Story 3.2 – Keyboard navigation standard
**Description**  
Standardize input handling.

**Rules**
- ↑ / ↓: list navigation
- ← / →: button groups
- Enter: confirm
- Esc: back / cancel

**Acceptance Criteria**
- No mouse required
- All screens respond consistently

---

# EPIC 4 – Match Card Hub Screen

## Story 4.1 – Hub layout
**Description**  
Primary landing screen.

**Components**
- Slot A card
- Slot B card
- Book Match button
- Notes line

**Acceptance Criteria**
- Clear focus indicator
- Single‑column layout

---

## Story 4.2 – Slot interaction
**Description**  
Allow selecting Wrestler A or B.

**Rules**
- Enter on slot opens selection modal

**Acceptance Criteria**
- Slot shows wrestler name or “Empty”
- Selecting replaces previous value

---

## Story 4.3 – Booking validation
**Description**  
Prevent invalid matches.

**Rules**
- Both slots required
- A ≠ B

**Acceptance Criteria**
- Book button disabled until valid

---

# EPIC 5 – Wrestler Selection Modal

## Story 5.1 – Wrestler list
**Description**  
Scrollable list of wrestlers.

**Acceptance Criteria**
- Arrow keys move highlight
- Long lists scroll

---

## Story 5.2 – Wrestler detail preview
**Description**  
Show stats of highlighted wrestler.

**Acceptance Criteria**
- Alignment, popularity, stamina visible
- Updates as highlight changes

---

## Story 5.3 – Lock opponent
**Description**  
Prevent selecting the already chosen opponent.

**Acceptance Criteria**
- Locked wrestler cannot be selected
- Clear visual indicator

---

# EPIC 6 – Confirm Booking Modal

## Story 6.1 – Confirmation layout
**Description**  
Final check before simulation.

**Contents**
- “A vs B”
- Key stats summary

**Acceptance Criteria**
- No editing possible here

---

## Story 6.2 – Confirm / Back actions
**Acceptance Criteria**
- Enter on Confirm starts simulation
- Esc returns to Hub

---

# EPIC 7 – Simulating Screen

## Story 7.1 – Simulation pacing
**Description**  
Short non‑interactive screen.

**Acceptance Criteria**
- Shows spinner or text
- Auto‑advances after delay

---

# EPIC 8 – Results Screen

## Story 8.1 – Winner & rating display
**Acceptance Criteria**
- Winner name prominent
- Rating clearly visible

---

## Story 8.2 – Stat changes table
**Description**  
Before → after presentation.

**Acceptance Criteria**
- Popularity and stamina shown
- Easy to read on mobile terminal

---

## Story 8.3 – Post‑match actions
**Actions**
- Book Another (reset)
- Rematch (reuse A & B)
- Quit

**Acceptance Criteria**
- Correct state transitions

---

# EPIC 9 – Testing & Quality

## Story 9.1 – Determinism tests
**Acceptance Criteria**
- Same seed yields same result

---

## Story 9.2 – Validation tests
**Acceptance Criteria**
- Invalid bookings blocked

---

## Story 9.3 – Boundary tests
**Acceptance Criteria**
- Stats never exceed bounds

---

# EPIC 10 – Definition of Done

The vertical slice is complete when:
- Entire loop is playable end‑to‑end
- Keyboard‑only navigation works everywhere
- Simulation is deterministic
- UI is readable on narrow terminals
- No crashes or dead ends

---

**Explicitly Out of Scope**
- Multi‑match cards
- Storylines or feuds
- AI bookers
- Explanation of match outcomes
- Persistence or saves
