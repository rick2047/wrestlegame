# The Guide — Wrestling GM Game

> A living product and design guide for a wrestling promotion management game inspired by modern GM modes.

---

## 1. Vision Statement

The vision of this game is to create a **deep yet approachable wrestling promotion management experience**
where players take on the role of a General Manager, balancing **creative booking, business strategy, and
talent management** to build the most successful wrestling brand.

The experience centers on **meaningful weekly decisions**—how shows are booked, how wrestlers are developed,
and how limited resources are allocated—so that every choice has visible consequences on popularity, morale,
finances, and long-term growth.

Rather than being a pure simulation or spreadsheet-driven optimizer, the game emphasizes **dramatic
storytelling through systems**. Rivalries emerge from player decisions, stars rise or fall based on
momentum and fatigue, and each promotion gradually develops a distinct identity. The goal is for players
to feel both the **pressure and satisfaction** of running a wrestling promotion week after week.

---

## 2. Design Pillars (Draft)

- **Every Decision Has a Cost** – Time, money, stamina, or morale.
- **Systems Create Stories** – Narrative emerges from mechanics, not scripts.
- **Constraints Drive Creativity** – Limited resources are a feature, not friction.
- **Readable, Not Overwhelming** – Depth without micromanagement.

---

## 3. Current UI State (Vertical Slice 1)

This section reflects the UI as implemented today. It should be updated as new
vertical slices expand or revise the interface.

### 3.1 User Flow

1. **Launch app** -> Match Card Hub
2. Select **Slot A** -> open wrestler selector modal -> confirm selection
3. Select **Slot B** -> open wrestler selector modal -> confirm selection
4. Press **Book Match** -> open **Confirm Booking** modal
5. Confirm -> Simulating screen
6. Auto-advance -> Results screen
7. Choose:
   - **Book Another Match** -> back to Match Card Hub (slots cleared)
   - **Re-match** -> Simulating -> Results (same A/B)

### 3.2 Screens

**A) Match Card Hub**
- Shows Slot A and Slot B "cards"
- Each slot opens a selector modal
- Displays a reactive Notes line (e.g., Face vs Heel bonus)
- Primary button: **Book Match** (disabled until both slots selected and A != B)
- Navigation is **arrow-key centered**:
  - `up/down` moves focus between Slot A card, Slot B card, and Book Match
  - `enter` activates the focused control

**B) Select Wrestler Modal (Slot A / Slot B)**
- List of wrestlers
- Detail panel for highlighted wrestler (alignment, popularity, stamina)
- Validation: the already-selected opponent is shown as locked/unselectable
- Navigation:
  - `up/down` moves selection within the roster list
  - `enter` confirms the highlighted wrestler
  - `esc` cancels and returns to hub

**C) Confirm Booking Modal**
- Summary: `A vs B` + key stats
- Optional: short "prediction" line (e.g., expected rating range)
- Navigation:
  - `left/right` switches between **Confirm** and **Back** buttons
  - `enter` activates the focused button
  - `esc` is equivalent to **Back**

**D) Simulating Screen**
- Brief "Simulating..." step for pacing (progress bar or spinner)
- No player input required

**E) Results Screen**
- Winner (prominent)
- Rating (prominent)
- Stat changes table:
  - Popularity: before -> after
  - Stamina: before -> after
- Actions:
  - **Book Another Match** (clears slots)
  - **Re-match** (same A/B)
- Navigation:
  - `up/down` moves focus between action buttons
  - `enter` activates the focused action
  - `esc` returns to hub (optional)

### 3.3 UI Flow, Focus Model and Hotkeys

**Flow**
- Match Card Hub -> Select Wrestler (A) modal -> Hub (A filled)
- Match Card Hub -> Select Wrestler (B) modal -> Hub (B filled)
- Match Card Hub -> Confirm Booking modal -> Simulating -> Results
- Results -> Book Another Match (clear slots) OR Re-match (same A/B)

**Focus model**
- Navigation is arrow-key centered.
- `up/down` moves focus between controls (cards/buttons) or moves highlight in lists.
- `left/right` switches focus between buttons inside a modal button row.
- `enter` activates the focused control.
- `esc` closes the current modal / backs out one step.

**Hotkeys**
- Global: `up/down`, `left/right` (where applicable), `enter`, `esc`
- Match Card Hub: `up/down` focus Slot A / Slot B / Book Match, `enter` select
- Select Wrestler Modal: `up/down` move, `enter` pick, `esc` cancel
- Confirm Booking Modal: `left/right` toggle Confirm/Back, `enter` select, `esc` back
- Results: `up/down` focus action, `enter` select, `esc` (optional) return to hub

### 3.4 ASCII Screen Mockups (Reference)

**Match Card Hub (empty)**
```text
┌──────────────────────────────────────┐
│ THE GUIDE: WrestleGM                 │
│ Match Card                           │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ > Slot A                             │
│   [ Select Wrestler ]                │
│                                      │
│   Slot B                             │
│   [ Select Wrestler ]                │
│                                      │
│   Notes: —                           │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│   Book Match (disabled)              │
└──────────────────────────────────────┘

Keys: up/down Focus   enter Select   esc Back
```

**Select Wrestler Modal (A)**
```text
                 ┌──────────────────────┐
                 │ Select Wrestler (A)  │
                 ├──────────────────────┤
                 │ > Asha Blaze  (FACE) │
                 │   Rohan Steel (HEEL) │
                 │   Mina Kage   (HEEL) │
                 │   Leo Nova    (FACE) │
                 ├──────────────────────┤
                 │ Pop: 48   Sta: 90    │
                 ├──────────────────────┤
                 │ Enter Select         │
                 │ Esc   Cancel         │
                 └──────────────────────┘
```

**Confirm Booking Modal**
```text
                 ┌──────────────────────┐
                 │ Confirm Booking      │
                 ├──────────────────────┤
                 │ Asha Blaze (FACE)    │
                 │   Pop 48  Sta 90     │
                 │        vs            │
                 │ Rohan Steel (HEEL)   │
                 │   Pop 52  Sta 85     │
                 ├──────────────────────┤
                 │ > [ Confirm ] [ Back ]│
                 └──────────────────────┘

Keys: left/right Focus   enter Select   esc Back
```

**Simulating**
```text
┌──────────────────────────────────────┐
│ Simulating match...                  │
└──────────────────────────────────────┘

Asha Blaze (FACE)  vs  Rohan Steel (HEEL)

██████████████░░░░░░░░░░░░  57%
```

**Results (no "Why" in-scope)**
```text
┌──────────────────────────────────────┐
│ Match Result                         │
└──────────────────────────────────────┘

Winner: Rohan Steel (HEEL)
Rating: ★★★★☆ (78)

Stat Changes
┌──────────────────────────────────────┐
│ Asha Blaze                           │
│   Pop: 48 -> 47   (-1)               │
│   Sta: 90 -> 78   (-12)              │
│                                      │
│ Rohan Steel                          │
│   Pop: 52 -> 55   (+3)               │
│   Sta: 85 -> 76   (-9)               │
└──────────────────────────────────────┘

Actions
┌──────────────────────────────────────┐
│ > Book Another Match                 │
│   Re-match                           │
│   Quit                               │
└──────────────────────────────────────┘

Keys: up/down Focus   enter Select   esc Back
```

---

## 3.5 Match Types (Brainstorm Draft)

This section captures early notes for the upcoming match type slice. It is
intentionally lightweight and will evolve as the slice is implemented.

### Draft Match Type List (Placeholder)
- Singles
- Hardcore
- Ladder
- Steel Cage
- Falls Count Anywhere
- Submission
- Iron Man
- TLC
- Last Man Standing
- No DQ

### Proficiency (Simple Model)
- Each wrestler is either proficient or not in a given match type.
- Proficiency is a binary flag per wrestler per match type.
- Proficiency should be visible in selection and confirmation UI.

### Expected Simulation Impact (Draft)
- Rating
  - Base rating still driven by popularity and alignment.
  - Match type adds a modifier scaled by average proficiency (proficient pair performs better).
- Stamina Loss
  - Each match type has a base stamina cost (e.g., hardcore styles cost more).
  - Proficiency reduces stamina loss slightly for proficient wrestlers.
- Winner Odds
  - Optional: proficiency adds a small weight bump toward the proficient wrestler.

### UI Placement (Draft)
- Match type is selected on the Match Card Hub before booking.
- Hub notes line can reflect the selected match type and any synergy bonuses.

---

## 4. Core Gameplay Loop (Placeholder)

> To be expanded

- Plan the week
- Book the show
- Resolve outcomes
- Review results
- Adapt strategy

---

## 5. Systems Overview (Placeholder)

- Roster and Contracts
- Booking and Matches
- Promos and Rivalries
- Economy and Budgeting
- Popularity, Morale, Stamina

---

## 6. UX and Presentation (Placeholder)

- UI-first design
- Strong transitions between screens
- Clear cause -> effect feedback

---

## 7. Technical Direction (Draft)

- Web-first
- TypeScript-focused
- UI-heavy architecture
- Emphasis on iteration speed

---

## 8. Scope and Non-Goals (Placeholder)

> To be defined

---

## Vertical Slices

All vertical slice details live under `slices/`. The current completed slice is:
- `slices/vertical-slice-1.md`

---

Last updated: 2026-01-07
