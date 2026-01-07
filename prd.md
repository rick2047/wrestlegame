# The Guide — Wrestling GM Game

> A living product & design guide for a wrestling promotion management game inspired by modern GM modes.

---

## 1. Vision Statement

The vision of this game is to create a **deep yet approachable wrestling promotion management experience** where players take on the role of a General Manager, balancing **creative booking, business strategy, and talent management** to build the most successful wrestling brand.

The experience centers on **meaningful weekly decisions**—how shows are booked, how wrestlers are developed, and how limited resources are allocated—so that every choice has visible consequences on popularity, morale, finances, and long-term growth.

Rather than being a pure simulation or spreadsheet-driven optimizer, the game emphasizes **dramatic storytelling through systems**. Rivalries emerge from player decisions, stars rise or fall based on momentum and fatigue, and each promotion gradually develops a distinct identity. The goal is for players to feel both the **pressure and satisfaction** of running a wrestling promotion week after week.

---

## 2. Design Pillars (Draft)

- **Every Decision Has a Cost** – Time, money, stamina, or morale.
- **Systems Create Stories** – Narrative emerges from mechanics, not scripts.
- **Constraints Drive Creativity** – Limited resources are a feature, not friction.
- **Readable, Not Overwhelming** – Depth without micromanagement.

---

## 3. Vertical Slice PRD — Book One Match (TUI)

### 3.1 Goal

Deliver a **playable prototype** where the player can **book a single match** between two wrestlers and immediately **see a satisfying, readable result** (winner, rating, and stat changes).

### 3.2 Why This Slice

- Validates the **core fun**: booking choices → outcomes → consequences
- Produces a reusable **simulation core** that can later power any UI
- Keeps scope brutally small while still feeling like a “real product”

### 3.3 In Scope

**User actions**
- Choose Wrestler A
- Choose Wrestler B
- Confirm “Book Match”
- View match result and stat deltas
- Start over / book another match (same session)

**UI**
- Terminal UI (TUI) built with Textual
- Screens/modals in this slice:
  - Match Card Hub
  - Select Wrestler modal (for Slot A / Slot B)
  - Confirm Booking modal
  - Simulating screen
  - Results screen
- Basic transitions (e.g., fade/slide) to create game feel

**Simulation output**
- Winner
- Match rating (0–100 or 1–5 stars)
- Stat changes (before → after)

### 3.4 Out of Scope

- Weeks/seasons/calendar
- Money/budget
- Brands, rival GMs
- Rivalries/promos/storylines
- Multiple matches per show
- Match types, stipulations
- Contracts, injuries, morale
- Save/load
- Outcome explanation / "Why" text generation (future model/feature)

### 3.5 User Flow

1. **Launch app** → Match Card Hub
2. Select **Slot A** → open wrestler selector modal → confirm selection
3. Select **Slot B** → open wrestler selector modal → confirm selection
4. Press **Book Match** → open **Confirm Booking** modal
5. Confirm → Simulating screen
6. Auto-advance → Results screen
7. Choose:
   - **Book Another Match** → back to Match Card Hub (slots cleared)
   - **Re-match** → Simulating → Results (same A/B)

### 3.6 Screens

**A) Match Card Hub**
- Shows Slot A and Slot B “cards”
- Each slot opens a selector modal
- Displays a reactive Notes line (e.g., Face vs Heel bonus)
- Primary button: **Book Match** (disabled until both slots selected and A != B)
- Navigation is **arrow-key centered**:
  - `↑/↓` moves focus between Slot A card, Slot B card, and Book Match
  - `Enter` activates the focused control

**B) Select Wrestler Modal (Slot A / Slot B)**
- List of wrestlers
- Detail panel for highlighted wrestler (alignment, popularity, stamina)
- Validation: the already-selected opponent is shown as locked/unselectable
- Navigation:
  - `↑/↓` moves selection within the roster list
  - `Enter` confirms the highlighted wrestler
  - `Esc` cancels and returns to hub

**C) Confirm Booking Modal**
- Summary: `A vs B` + key stats
- Optional: short “prediction” line (e.g., expected rating range)
- Navigation:
  - `←/→` switches between **Confirm** and **Back** buttons
  - `Enter` activates the focused button
  - `Esc` is equivalent to **Back**

**D) Simulating Screen**
- Brief “Simulating…” step for pacing (progress bar or spinner)
- No player input required

**E) Results Screen**
- Winner (prominent)
- Rating (prominent)
- Stat changes table:
  - Popularity: before → after
  - Stamina: before → after
- Actions:
  - **Book Another Match** (clears slots)
  - **Re-match** (same A/B)
- Navigation:
  - `↑/↓` moves focus between action buttons
  - `Enter` activates the focused action
  - `Esc` returns to hub (optional)

### 3.7 Data Model (Minimum)

**Wrestler**
- id (string)
- name (string)
- alignment (Face | Heel)
- popularity (0–100)
- stamina (0–100)

**Match**
- wrestler_a_id
- wrestler_b_id

**MatchResult**
- winner_id
- loser_id
- rating
- deltas (popularity_delta, stamina_delta for each)

### 3.8 Match Resolution Rules (MVP)

Keep this intentionally simple and tune later.

**Rating**
- Base = average(popularity of both)
- Bonus if Face vs Heel (small)
- Penalty if either stamina is low (small)
- Random variance (small)
- Clamp to range

**Winner**
- Weighted by popularity and stamina (slight advantage), plus randomness

**Stat changes**
- Winner popularity increases (small)
- Loser popularity decreases or stays flat (tiny)
- Both stamina decrease (based on rating or fixed)

### 3.9 Acceptance Criteria

- Player can complete the loop in under ~30 seconds without reading instructions
- Results screen clearly shows **cause → effect** (before/after numbers)
- No crashes for invalid selections (A == B blocked)
- Simulation is deterministic under a fixed seed (for testing)

### 3.10 Tech Notes (Prototype)

- Build as a Python TUI app using **Textual**
- Use **uv** for Python package and environment management
- Keep simulation logic in pure Python modules (UI calls into it)
- Add a small test suite for the sim functions

### 3.11 Mobile Terminal & Reactivity Notes

**Mobile terminal friendliness (e.g., Android/Termux)**
- Design for narrow screens: default to **single-column layouts** with scroll
- Avoid dense multi-pane dashboards in the slice
- Prefer large, readable typography spacing and clear focus states

**Reactive UI behavior**
- Use Textual’s reactive state patterns so selections instantly update the context panel
- Results should feel “alive”: animate or step through before → after stat changes

**Optional later**
- Consider running the same UI in a browser via Textual’s web support if mobile terminal UX becomes limiting

### 3.12 UI Flow, Focus Model & Hotkeys

**Flow**
- Match Card Hub → Select Wrestler (A) modal → Hub (A filled)
- Match Card Hub → Select Wrestler (B) modal → Hub (B filled)
- Match Card Hub → Confirm Booking modal → Simulating → Results
- Results → Book Another Match (clear slots) OR Re-match (same A/B)

**Focus model**
- Navigation is arrow-key centered.
- `↑/↓` moves focus between controls (cards/buttons) or moves highlight in lists.
- `←/→` switches focus between buttons inside a modal button row.
- `Enter` activates the focused control.
- `Esc` closes the current modal / backs out one step.

**Hotkeys**
- Global: `↑/↓`, `←/→` (where applicable), `Enter`, `Esc`
- Match Card Hub: `↑/↓` focus Slot A / Slot B / Book Match, `Enter` select
- Select Wrestler Modal: `↑/↓` move, `Enter` pick, `Esc` cancel
- Confirm Booking Modal: `←/→` toggle Confirm/Back, `Enter` select, `Esc` back
- Results: `↑/↓` focus action, `Enter` select, `Esc` (optional) return to hub

### 3.13 ASCII Screen Mockups (Reference)

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

Keys: ↑↓ Focus   Enter Select   Esc Back
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

Keys: ←→ Focus   Enter Select   Esc Back
```

**Simulating**
```text
┌──────────────────────────────────────┐
│ Simulating match...                  │
└──────────────────────────────────────┘

Asha Blaze (FACE)  vs  Rohan Steel (HEEL)

██████████████░░░░░░░░░░░░  57%
```

**Results (no “Why” in-scope)**
```text
┌──────────────────────────────────────┐
│ Match Result                         │
└──────────────────────────────────────┘

Winner: Rohan Steel (HEEL)
Rating: ★★★★☆ (78)

Stat Changes
┌──────────────────────────────────────┐
│ Asha Blaze                           │
│   Pop: 48 → 47   (-1)                │
│   Sta: 90 → 78   (-12)               │
│                                      │
│ Rohan Steel                          │
│   Pop: 52 → 55   (+3)                │
│   Sta: 85 → 76   (-9)                │
└──────────────────────────────────────┘

Actions
┌──────────────────────────────────────┐
│ > Book Another Match                 │
│   Re-match                           │
│   Quit                               │
└──────────────────────────────────────┘

Keys: ↑↓ Focus   Enter Select   Esc Back
```

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

- Roster & Contracts
- Booking & Matches
- Promos & Rivalries
- Economy & Budgeting
- Popularity, Morale, Stamina

---

## 6. UX & Presentation (Placeholder)

- UI-first design
- Strong transitions between screens
- Clear cause → effect feedback

---

## 7. Technical Direction (Draft)

- Web-first
- TypeScript-focused
- UI-heavy architecture
- Emphasis on iteration speed

---

## 8. Scope & Non-Goals (Placeholder)

> To be defined

---

_Last updated: 2026-01-07_
