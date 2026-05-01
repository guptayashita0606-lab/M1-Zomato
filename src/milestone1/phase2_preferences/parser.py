from __future__ import annotations

from typing import Mapping

from .models import UserPreferences
from .validation import (
    FieldError,
    PreferencesValidationError,
    VALID_BUDGET_BANDS,
    normalize_budget_band,
    normalize_cuisines,
    normalize_rating,
    normalize_text,
)


def _value(mapping: Mapping[str, object], *keys: str) -> object:
    for key in keys:
        if key in mapping:
            return mapping[key]
    return ""


def preferences_from_mapping(
    mapping: Mapping[str, object],
    *,
    allowed_city_names: set[str] | None = None,
    max_additional_length: int = 300,
) -> UserPreferences:
    location_raw = _value(mapping, "location", "city")
    budget_raw = _value(mapping, "budget_band", "budget")
    cuisines_raw = _value(mapping, "cuisines", "cuisine")
    rating_raw = _value(mapping, "minimum_rating", "min_rating", "rating")
    additional_raw = _value(mapping, "additional_preferences", "additional", "notes")

    location = normalize_text(location_raw)
    budget_band = normalize_budget_band(budget_raw)
    cuisines = normalize_cuisines(cuisines_raw)
    minimum_rating = normalize_rating(rating_raw)
    additional_preferences = str(additional_raw or "").strip()

    errors: list[FieldError] = []
    if not location:
        errors.append(FieldError("location", "Location is required."))
    elif allowed_city_names is not None and location not in allowed_city_names:
        errors.append(
            FieldError(
                "location",
                "Unknown location for current corpus. Use a supported city name.",
            )
        )

    if budget_band not in VALID_BUDGET_BANDS:
        errors.append(
            FieldError(
                "budget_band",
                "Budget band must be one of: low, medium, high.",
            )
        )

    if not cuisines:
        errors.append(FieldError("cuisines", "At least one cuisine is required."))

    if minimum_rating is None:
        errors.append(FieldError("minimum_rating", "Minimum rating must be a number from 0 to 5."))

    if len(additional_preferences) > max_additional_length:
        errors.append(
            FieldError(
                "additional_preferences",
                f"Additional preferences must be <= {max_additional_length} characters.",
            )
        )

    if errors:
        raise PreferencesValidationError(errors)

    return UserPreferences(
        location=location,
        budget_band=budget_band,
        cuisines=cuisines,
        minimum_rating=minimum_rating,
        additional_preferences=additional_preferences,
    )
