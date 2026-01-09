WrestleGM – Textual‑First Product Requirements Document (Vertical Slice)

> This document supersedes earlier PRDs and merges Vertical Slice 1 & 2.
Match Types are data‑driven and affect simulation, while remaining within a single‑match vertical slice.




---

1. Purpose

This document defines the Textual-first PRD for the WrestleGM vertical slice.

> Intentional scope note: This PRD intentionally includes architectural, simulation, and data contracts in addition to product and UX requirements. This is a deliberate choice to eliminate ambiguity in a small-team / solo development environment.



Scope is strictly limited to booking and simulating a single match end-to-end in a terminal UI.


---

2. Core Principles

Textual widgets are the source of UI consistency

ASCII mockups describe structure, not rendering

Keyboard‑only navigation is mandatory

Deterministic simulation (seeded RNG)

Narrow terminal support (≤40 chars width)

Match rules are data‑driven, not hardcoded



---

3. Data & Domain Model

This section defines all data-driven domain entities loaded at application startup. No domain entities are hardcoded in code.


---

3.1 WrestlerDefinition

id: string (stable, unique)

name: string

alignment: Face | Heel

popularity: number (0–100)

stamina: number (0–100)


Loaded from data/wrestlers.json.


---

3.2 MatchTypeDefinition

id: string (stable, unique)

name: string

description: string (optional)

modifiers:

rating_bonus

rating_variance

stamina_cost_winner

stamina_cost_loser

popularity_delta_winner

popularity_delta_loser



Loaded from data/match_types.json.


---

4. State Management

Global application state is the single source of truth.

4.1 State Fields

selected_a_id

selected_b_id

match_type_id

last_result

seed


4.2 State Ownership Rules

Screens may read state but never own it

Simulation produces results but never mutates state

UI layer explicitly applies stat deltas

Rematch preserves all selection state

New Match resets all selection state



---

5. UI System & Navigation

3.1 ASCII vs Textual Responsibility

ASCII in this PRD describes:

Screen structure

Information hierarchy

Focus intent


Textual is responsible for:

Borders and framing

Focus highlights

Disabled states

Layout spacing



No screen may render custom ASCII strings for layout outside of Textual widgets.


---

3.2 Global Navigation Contract

Global

Esc → Back / Cancel / Close modal

No mouse usage anywhere


Lists

↑ / ↓ → Move selection

Enter → Select


Button Groups

← / → → Switch button focus

Enter → Activate


Only one focus context may be active at a time.


---

4. Match Types & Simulation Modifiers (Merged from Slices)

4.1 Match Type Model (Data‑Driven)

Match types are loaded from configuration at startup.

MatchTypeDefinition

id: str — stable key (e.g. singles, no_dq, hardcore)

name: str — display name

description: str — optional

modifiers:

rating_bonus: int

rating_variance: int

stamina_cost_winner: int

stamina_cost_loser: int

popularity_delta_winner: int

popularity_delta_loser: int



Match

wrestler_a_id

wrestler_b_id

match_type_id


No simulation logic may assume specific match types exist.


---

4.2 Match Type Data Source

Loaded from data/match_types.json

Vertical slice ships with a small default set

IDs must be unique and stable

Adding a new match type must not require code changes



---

4.3 Simulation Contract (Updated)

simulate_match(match, roster, match_types, seed) -> MatchResult

Rules:

All randomness flows through seeded RNG

Match type modifiers apply additively

Stats remain the primary determinant of winner

Increased variance may allow more upsets, but never guarantees them



---

4.4 Match Result Auditability

MatchResult must include:

match_type_id

match_type_name

applied_modifiers


This enables debugging, replay verification, and future analytics.


---

5. Screen‑by‑Screen Textual Mapping

This section is authoritative. Each screen defines:

Conceptual ASCII layout

Required Textual widgets

Focus & navigation rules



---

5.1 Match Card Hub (Reference Screen)

Conceptual Layout

┌────────────────────────────┐
│ MATCH CARD                 │
├────────────────────────────┤
│ Slot A: [ Empty ]          │
│ Slot B: [ Empty ]          │
│ Type : Singles             │
│                            │
│ [ Book Match ]             │
└────────────────────────────┘

Textual Composition

Screen

Root Container

Static (title)

Button (Slot A)

Button (Slot B)

Button or Select (Match Type)

Primary Button (Book Match)


Behavior

Slot buttons open Wrestler Selection modal

Match Type opens Match Type Selection modal

Book Match disabled until A, B, and Type are valid



---

5.2 Wrestler Selection Modal

Conceptual Layout

┌────────────────────────────┐
│ SELECT WRESTLER            │
├────────────────────────────┤
│ > John Steel               │
│   Max Power                │
│   Night Fang               │
│                            │
│ Pop: 72  Sta: 65  Face     │
└────────────────────────────┘

Textual Composition

ModalScreen

Container (horizontal split)

ListView (wrestler list)

Static (detail preview)


Behavior

Locked opponent disabled in list

Enter selects wrestler

Esc cancels



---

5.3 Match Type Selection Modal

Conceptual Layout

┌────────────────────────────┐
│ SELECT MATCH TYPE          │
├────────────────────────────┤
│ > Singles                  │
│   No DQ                    │
│   Hardcore                 │
└────────────────────────────┘

Textual Composition

ModalScreen

ListView (match types)


Behavior

Enter selects type

Esc cancels



---

5.4 Confirm Booking Modal

Conceptual Layout

┌────────────────────────────┐
│ CONFIRM MATCH              │
├────────────────────────────┤
│ John Steel vs Max Power    │
│ Type: Singles              │
│                            │
│ [ Confirm ]   [ Back ]     │
└────────────────────────────┘

Textual Composition

ModalScreen

Static (summary)

Horizontal container

Two Button widgets


Behavior

No editing allowed

Confirm triggers simulation



---

5.5 Simulating Screen

Conceptual Layout

┌────────────────────────────┐
│ SIMULATING MATCH...        │
│                            │
│ Please wait                │
└────────────────────────────┘

Textual Composition

Screen

Static

Optional LoadingIndicator


Behavior

Non‑interactive

Auto‑advance after delay



---

5.6 Results Screen

Conceptual Layout

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

Textual Composition

Screen

Static (result header)

Static (stat table)

Horizontal button row


Behavior

Rematch keeps selections and match type

New resets all state

Quit exits app



---

7. Definition of Done

The vertical slice is complete when:

Full loop playable end‑to‑end

Match types affect simulation deterministically

Match types are data‑driven

All screens use defined Textual composition

Keyboard navigation works everywhere

UI readable at ≤40 chars width



---

8. Explicitly Out of Scope

Multi‑match cards

Storylines or feuds

AI bookers

Persistence / saves



---

9. Implementation Guide (Merged Summary)

This section merges and normalises the WrestleGM Vertical Slice Guide into this PRD, making this document the single source of truth for both product intent and implementation direction.

The guide content is incorporated here at a design-contract level (what must exist and how responsibilities are split), not as step-by-step developer instructions.


---

9.1 Architectural Boundaries

The application is structured into three explicit layers:

UI Layer (Textual)

Screens, modals, widgets

Keyboard navigation & focus

No business logic


Domain Layer

Wrestler

Match

MatchTypeDefinition

MatchResult


Simulation Layer

Deterministic RNG

Winner calculation

Rating calculation

Stat delta calculation

Match-type modifier application


No layer may directly bypass another.


---

9.2 Deterministic Simulation Flow (Authoritative)

The simulation flow must follow this exact order:

1. Resolve MatchTypeDefinition via match_type_id


2. Compute effective stats (base + modifiers)


3. Determine winner using weighted stats + variance


4. Calculate match rating (base + type bonus + variance)


5. Calculate stat deltas (winner/loser, stamina, popularity)


6. Return immutable MatchResult



No UI state mutation is allowed during simulation.


---

9.3 RNG & Reproducibility

All randomness flows through a single RNG instance

RNG must be seeded from app state

Same seed + same inputs must always yield the same MatchResult


This guarantees:

Testability

Replay consistency

Future save/load compatibility



---

9.4 UI Flow Contract

The full vertical slice flow is:

1. Match Card Hub


2. Wrestler Selection Modal (Slot A)


3. Wrestler Selection Modal (Slot B)


4. Match Type Selection Modal


5. Confirm Booking Modal


6. Simulating Screen


7. Results Screen



No screen skipping is allowed.


---

9.5 State Ownership Rules

App state is the single source of truth

Screens may read state but not own it

Simulation produces results but does not apply them

UI layer applies stat deltas explicitly



---

9.6 Testing Expectations (From Guide)

Minimum required tests:

Determinism test (same seed, same result)

Boundary tests (stats never exceed 0–100)

Match type modifier tests

Invalid booking prevention tests



---

9.7 Definition of Done (Expanded)

The vertical slice is complete only when:

Match types are configurable and simulation-affecting

Simulation is deterministic and test-covered

UI uses Textual widgets exclusively

Keyboard-only navigation works on all screens

Narrow terminals render correctly

No crashes or dead ends exist



---

9.8 Guide Supersession Note

This PRD supersedes the standalone guide.

Any future changes must update this document directly rather than reintroducing parallel specs.


---

10. Data-Driven Domain Definitions

Both Wrestlers and Match Types are loaded from external JSON configuration files at application startup. No domain entities are hardcoded in code.


---

10.1 Wrestler Data

WrestlerDefinition Model

id: string (stable, unique)

name: string

alignment: "Face" | "Heel"

popularity: number (0–100)

stamina: number (0–100)


Data Source

Loaded from data/wrestlers.json

Vertical slice ships with a small default roster (6–10 wrestlers)

IDs must be unique and stable


Example data/wrestlers.json

{
  "wrestlers": [
    {
      "id": "john_steel",
      "name": "John Steel",
      "alignment": "Face",
      "popularity": 75,
      "stamina": 80
    },
    {
      "id": "max_power",
      "name": "Max Power",
      "alignment": "Heel",
      "popularity": 68,
      "stamina": 85
    },
    {
      "id": "night_fang",
      "name": "Night Fang",
      "alignment": "Heel",
      "popularity": 72,
      "stamina": 70
    }
  ]
}


---

10.2 Match Type Data

MatchTypeDefinition Model

id: string (stable, unique)

name: string

description: string (optional)

modifiers:

rating_bonus: number

rating_variance: number

stamina_cost_winner: number

stamina_cost_loser: number

popularity_delta_winner: number

popularity_delta_loser: number



Data Source

Loaded from data/match_types.json

Vertical slice ships with a small default set

Adding a new match type must not require code changes


Example data/match_types.json

{
  "match_types": [
    {
      "id": "singles",
      "name": "Singles",
      "description": "Standard one-on-one match",
      "modifiers": {
        "rating_bonus": 0,
        "rating_variance": 5,
        "stamina_cost_winner": 10,
        "stamina_cost_loser": 12,
        "popularity_delta_winner": 4,
        "popularity_delta_loser": -2
      }
    },
    {
      "id": "no_dq",
      "name": "No Disqualification",
      "description": "Weapons allowed, higher risk",
      "modifiers": {
        "rating_bonus": 5,
        "rating_variance": 10,
        "stamina_cost_winner": 14,
        "stamina_cost_loser": 16,
        "popularity_delta_winner": 6,
        "popularity_delta_loser": -3
      }
    },
    {
      "id": "hardcore",
      "name": "Hardcore",
      "description": "Extreme rules, very high variance",
      "modifiers": {
        "rating_bonus": 10,
        "rating_variance": 18,
        "stamina_cost_winner": 20,
        "stamina_cost_loser": 22,
        "popularity_delta_winner": 8,
        "popularity_delta_loser": -4
      }
    }
  ]
}


---

Contractual Rule:

Simulation and UI must rely exclusively on loaded data.

Changing balance values or adding content must not require code changes.
