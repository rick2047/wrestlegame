# UI Flow

## Screen Map
- **Hub**: choose Slot A and Slot B, then book the match.
- **Selector (Modal)**: scrollable roster, stats preview, opponent locked.
- **Match Type Selector (Modal)**: scrollable list of match types.
- **Confirm (Modal)**: review A vs B, confirm or go back.
- **Simulating**: short pacing screen that auto-advances.
- **Results**: winner, rating, stat changes, and post-match actions.

## Navigation Model
Primary keys are arrow-driven, with fallbacks for terminals with limited key support.

- Hub / Results:
  - `Up` / `Down`: move focus.
  - `j`/`k` or `w`/`s`: fallback focus navigation.
  - `Enter`: activate focused action.
- Selector:
  - `Up` / `Down`: move roster highlight.
  - `j`/`k` or `w`/`s`: fallback list navigation.
  - `Enter`: select highlighted wrestler.
  - `Esc`: cancel.
- Match Type Selector:
  - `Up` / `Down`: move list highlight.
  - `j`/`k` or `w`/`s`: fallback list navigation.
  - `Enter`: select highlighted match type.
  - `Esc`: cancel.
- Confirm:
  - `Left` / `Right`: move between buttons.
  - `h`/`l` or `a`/`d`: fallback left/right navigation.
  - `Enter`: confirm focused button.
  - `Esc`: back.

## Focus Strategy
Each screen sets an initial focus target on mount to ensure keyboard navigation works immediately. When in doubt, use `Tab`/`Shift+Tab` to move focus.

## Hub Notes Line
The hub displays a reactive note based on the selected wrestlers:
- Face vs Heel: shows bonus note.
- Same alignment: shows a neutral note.
- One or both empty: shows “—”.
When a match type is selected, the hub appends the match type name to the note.

## Cancel Behavior
Cancelling the wrestler or match type selection modal preserves the prior selection.
