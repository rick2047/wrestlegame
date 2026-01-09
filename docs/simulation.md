# Simulation

## Determinism
All randomness is seed-driven. The simulation accepts a seed and uses a local RNG wrapper so the same seed yields identical results. The UI increments the seed after each simulation to keep a predictable sequence.

## Winner Calculation
Each wrestler gets a weight:
- `popularity + stamina + proficiency_bonus + random(-5..5)`
The RNG picks a winner using weighted choice. Higher stats win more often, but upsets remain possible.

## Rating Calculation
Rating is clamped to 0–100 and computed as:
- Base: average popularity of both wrestlers.
- Bonus: +5 if Face vs Heel.
- Match type bonus: `rating_bonus` from the selected match type.
- Proficiency bonus: small bonus if one or both wrestlers are proficient.
- Penalty: -5 for each wrestler with stamina < 40.
- Variance: random(-rating_variance..rating_variance).

## Stat Deltas
After the match:
- Winner popularity: `popularity_delta_winner`
- Loser popularity: `popularity_delta_loser`
- Stamina: `stamina_cost_winner` / `stamina_cost_loser` + random(0..2)
- Proficient wrestlers lose 2 less stamina in the selected match type

All resulting stats are clamped to 0–100 by `apply_result()`.

## Result Audit Fields
Each match result includes:
- `match_type_id`
- `match_type_name`
- `applied_modifiers`

## Extending the Model
If you add new match rules, keep these constraints:
- Pure function for simulation (no UI state).
- Explicit deltas in the result.
- Determinism under fixed seed.
