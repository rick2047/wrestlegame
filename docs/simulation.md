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
- Match type bonus: fixed bonus per match type.
- Proficiency bonus: small bonus if one or both wrestlers are proficient.
- Penalty: -5 for each wrestler with stamina < 40.
- Variance: random(-5..5).

## Stat Deltas
After the match:
- Winner popularity: +3
- Loser popularity: -1
- Stamina: base cost per match type + random(0..4)
- Proficient wrestlers lose 2 less stamina in the selected match type

All resulting stats are clamped to 0–100 by `apply_result()`.

## Extending the Model
If you add new match rules, keep these constraints:
- Pure function for simulation (no UI state).
- Explicit deltas in the result.
- Determinism under fixed seed.
