from __future__ import annotations

import json
from typing import Any

from milestone1.phase2_preferences import UserPreferences

from .filters import Candidate


def build_prompt_payload(
    preferences: UserPreferences,
    candidates: list[Candidate],
) -> dict[str, Any]:
    candidate_rows: list[dict[str, Any]] = []
    for item in candidates:
        candidate_rows.append(
            {
                "candidate_id": item.candidate_id,
                "name": item.restaurant.name,
                "location": item.restaurant.location,
                "cuisines": item.restaurant.cuisines,
                "cost": item.restaurant.cost,
                "rating": item.restaurant.rating,
            }
        )

    preference_obj = {
        "location": preferences.location,
        "budget_band": preferences.budget_band,
        "cuisines": preferences.cuisines,
        "minimum_rating": preferences.minimum_rating,
        "additional_preferences": preferences.additional_preferences,
    }

    system_instructions = (
        "You are a restaurant recommendation assistant. "
        "Recommend only from the provided candidate list. "
        "Never invent restaurants not present in candidates. "
        "Return JSON with key `rankings`, where each item has "
        "`candidate_id`, `rank`, and `explanation`."
    )
    user_prompt = (
        "User preferences:\n"
        + json.dumps(preference_obj, indent=2)
        + "\n\nCandidates:\n"
        + json.dumps(candidate_rows, indent=2)
        + "\n\nReturn top recommendations grounded only in candidates."
    )
    return {
        "system_instructions": system_instructions,
        "user_prompt": user_prompt,
        "preferences": preference_obj,
        "candidates": candidate_rows,
    }
