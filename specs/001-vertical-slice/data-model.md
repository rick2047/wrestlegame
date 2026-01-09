# Data Model

## WrestlerDefinition

Fields:
- id: string (unique, stable)
- name: string
- alignment: "Face" | "Heel"
- popularity: integer (0-100)
- stamina: integer (0-100)

Validation rules:
- id unique across roster
- popularity and stamina clamped to 0-100
- alignment must be one of the allowed values

## MatchTypeDefinition

Fields:
- id: string (unique, stable)
- name: string
- description: string (optional)
- modifiers:
  - rating_bonus: integer
  - rating_variance: integer
  - stamina_cost_winner: integer
  - stamina_cost_loser: integer
  - popularity_delta_winner: integer
  - popularity_delta_loser: integer

Validation rules:
- id unique across match types
- all modifier fields are integers

## Match

Fields:
- wrestler_a_id: string (references WrestlerDefinition.id)
- wrestler_b_id: string (references WrestlerDefinition.id)
- match_type_id: string (references MatchTypeDefinition.id)

Validation rules:
- wrestler_a_id and wrestler_b_id must be distinct
- all referenced ids must exist in loaded data

## MatchResult

Fields:
- match_type_id: string
- match_type_name: string
- applied_modifiers: object (same shape as MatchTypeDefinition.modifiers)
- winner_id: string
- loser_id: string
- rating: integer or rating band
- popularity_delta_winner: integer
- popularity_delta_loser: integer
- stamina_cost_winner: integer
- stamina_cost_loser: integer

Validation rules:
- match_type_id and match_type_name must match a known match type
- applied_modifiers must reflect the selected match type

## AppState

Fields:
- selected_a_id: string | null
- selected_b_id: string | null
- match_type_id: string | null
- last_result: MatchResult | null
- seed: string | integer

State transitions:
- New Match: clear selected_a_id, selected_b_id, match_type_id, last_result
- Rematch: keep selected_a_id, selected_b_id, match_type_id, clear last_result
- Confirm Booking: create Match from current selections
- Simulation Complete: set last_result with returned MatchResult

Relationships:
- AppState holds current Match selections and last MatchResult
- Match references WrestlerDefinition and MatchTypeDefinition
- MatchResult references MatchTypeDefinition for auditing
