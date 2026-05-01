from __future__ import annotations

from typing import Any


class SchemaAssertionError(ValueError):
    """Raised when source dataset schema misses required fields."""


REQUIRED_CANONICAL_FIELDS = ("name", "location", "cuisines", "cost", "rating")

# Common upstream aliases for expected source columns.
SOURCE_FIELD_CANDIDATES: dict[str, tuple[str, ...]] = {
    "name": ("restaurant_name", "name", "res_name", "restaurant"),
    "location": ("location", "city", "locality"),
    "cuisines": ("cuisines", "cuisine", "food_type"),
    "cost": (
        "average_cost_for_two",
        "approx_cost(for two people)",
        "cost",
        "price",
        "cost_for_two",
    ),
    "rating": ("aggregate_rating", "rate", "rating", "avg_rating", "user_rating"),
}


def assert_source_schema(sample_row: dict[str, Any]) -> dict[str, str]:
    """Return canonical->source mapping for a sample row or raise."""
    row_keys = {str(key).strip().lower(): key for key in sample_row.keys()}
    mapping: dict[str, str] = {}
    missing: list[str] = []

    for canonical_name in REQUIRED_CANONICAL_FIELDS:
        matched_key = None
        for candidate in SOURCE_FIELD_CANDIDATES[canonical_name]:
            if candidate in row_keys:
                matched_key = row_keys[candidate]
                break
        if not matched_key:
            missing.append(canonical_name)
            continue
        mapping[canonical_name] = matched_key

    if missing:
        raise SchemaAssertionError(
            f"Missing required source fields for canonical mapping: {', '.join(missing)}"
        )
    return mapping
