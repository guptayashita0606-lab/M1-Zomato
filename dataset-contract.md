# Dataset Contract (v1)

Source dataset:
- [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)

## Supported Internal Fields

The v1 pipeline should normalize source fields into this internal contract:

- `name` (string): restaurant name
- `location` (string): normalized city/locality
- `cuisines` (list[string]): cuisine tags
- `cost` (string or numeric band): normalized cost/budget representation
- `rating` (float): normalized rating value
- `metadata` (object): optional extra source columns used for prompt grounding

## Contract Rules

- Required fields for recommendation: `name`, `location`, `cuisines`, `cost`, `rating`.
- `rating` must be numeric after normalization.
- Missing required fields should be dropped or handled by explicit fallback policy.
- Duplicate records should be resolved deterministically.
- Source schema must be asserted at ingestion time; fail fast on breaking changes.

## Mapping Policy (Phase 1)

Current canonical mapping candidates are resolved in this order:

- `name`: `restaurant_name` | `name` | `res_name` | `restaurant`
- `location`: `location` | `city` | `locality`
- `cuisines`: `cuisines` | `cuisine` | `food_type`
- `cost`: `average_cost_for_two` | `cost` | `price` | `cost_for_two`
- `rating`: `aggregate_rating` | `rating` | `avg_rating` | `user_rating`

Any source column rename or format change must update:
- `src/milestone1/phase1_ingestion/schema.py`
- this contract file
- related tests under `tests/`
