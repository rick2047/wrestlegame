# Vertical Slice PRD — Match Types (TUI)

## Goal
Add match types to the booking flow so the selected type affects simulation
(rating and stamina loss) and each wrestler has a simple proficiency flag.

## Why This Slice
- Expands booking depth without adding new game systems.
- Creates immediate, readable variation in match outcomes.
- Establishes a reusable pattern for match modifiers.

## In Scope
**User actions**
- Choose Wrestler A
- Choose Wrestler B
- Choose Match Type
- Confirm "Book Match"
- View result with match type context and stat deltas
- Start over / book another match (same session)

**UI**
- Match type selection on the Match Card Hub
- Match type shown in Confirm Booking and Results
- Proficiency visible in selector and/or confirmation

**Simulation output**
- Winner
- Match rating (0-100)
- Stat changes (before -> after)
- Match type context

## Out of Scope
- Match types changing winners via complex rules
- Stipulations with unique win conditions
- Match type-specific animations or visuals
- Multi-match cards
- Save/load or persistence

## User Flow
1. Launch app -> Match Card Hub
2. Select Slot A -> open wrestler selector modal -> confirm selection
3. Select Slot B -> open wrestler selector modal -> confirm selection
4. Select Match Type on hub
5. Press Book Match -> open Confirm Booking modal
6. Confirm -> Simulating screen
7. Auto-advance -> Results screen
8. Choose Book Another Match or Re-match

## Screens (Delta from Slice 1)
**Match Card Hub**
- Adds a Match Type control (button or list)
- Notes line can reference match type and alignment bonus
- Book Match disabled until A, B, and match type are selected

**Select Wrestler Modal**
- Shows proficiency for the currently selected match type
- Locked opponent still unselectable

**Confirm Booking Modal**
- Shows match type and per-wrestler proficiency

**Results Screen**
- Shows match type alongside rating

## ASCII Screen Mockups (Draft)

**Select Match Type Modal**
```text
                 ┌────────────────────────┐
                 │ Select Match Type      │
                 ├────────────────────────┤
                 │ > Singles              │
                 │   Hardcore             │
                 │   Ladder               │
                 │   Steel Cage           │
                 │   Falls Count Anywhere │
                 │   Submission           │
                 │   Iron Man             │
                 │   TLC                  │
                 │   Last Man Standing    │
                 │   No DQ                │
                 ├────────────────────────┤
                 │ Enter Select           │
                 │ Esc   Cancel           │
                 └────────────────────────┘
```

**Confirm Booking Modal (with Match Type)**
```text
                 ┌──────────────────────────┐
                 │ Confirm Booking          │
                 ├──────────────────────────┤
                 │ Match Type: Steel Cage   │
                 │                          │
                 │ Asha Blaze (FACE)        │
                 │   Pop 48  Sta 90  Pro: Y │
                 │        vs                │
                 │ Rohan Steel (HEEL)       │
                 │   Pop 52  Sta 85  Pro: N │
                 ├──────────────────────────┤
                 │ > [ Confirm ] [ Back ]   │
                 └──────────────────────────┘

Keys: left/right Focus   enter Select   esc Back
```

## Data Model (Additions)
**MatchType**
- Enum or literal set of common types (about 10)
- Examples: Singles, Hardcore, Ladder, Steel Cage, Falls Count Anywhere,
  Submission, Iron Man, TLC, Last Man Standing, No DQ

**Wrestler**
- Adds `match_type_proficiency` mapping or set
- Simple binary proficiency per match type

**Match**
- Adds `match_type`

## Match Resolution Rules (Additions)
**Rating**
- Base rating from popularity and alignment, as before
- Match type adds a modifier
- Proficiency increases the modifier when both wrestlers are proficient

**Stamina Loss**
- Each match type has a base stamina cost
- Proficient wrestlers lose slightly less stamina

**Winner Odds**
- Optional small weight bump for proficient wrestlers in the selected type

## Acceptance Criteria
- Match type must be selected before booking
- Match type is visible on Confirm and Results screens
- Proficiency is visible during selection or confirmation
- Rating and stamina loss change based on match type
- Determinism preserved under fixed seed

## Implementation Map (Planned)
- Domain models: `domain/models.py`
- Roster proficiency data: `domain/roster.py`
- Simulation adjustments: `sim/engine.py`
- UI updates: `ui/hub.py`, `ui/selector.py`, `ui/confirm.py`, `ui/results.py`
- App state: `ui/state.py`, `app.py`
- Tests: `tests/`
