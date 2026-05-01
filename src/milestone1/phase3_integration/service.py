from __future__ import annotations

from typing import Any

from milestone1.phase1_ingestion import load_restaurants
from milestone1.phase2_preferences import UserPreferences

from .filters import Candidate, filter_and_rank
from .prompt import build_prompt_payload


def build_integration_output(
    preferences: UserPreferences,
    *,
    source: str = "hf",
    local_path: str | None = None,
    load_limit: int | None = 2000,
    candidate_cap: int = 25,
) -> dict[str, Any]:
    restaurants = load_restaurants(source=source, local_path=local_path, limit=load_limit)
    candidates = filter_and_rank(restaurants, preferences, candidate_cap=candidate_cap)
    payload = build_prompt_payload(preferences, candidates)
    return {
        "source": source,
        "load_limit": load_limit,
        "candidate_cap": candidate_cap,
        "candidate_count": len(candidates),
        "candidates": _serialize_candidates(candidates),
        "prompt_payload": payload,
    }


def _serialize_candidates(candidates: list[Candidate]) -> list[dict[str, Any]]:
    data: list[dict[str, Any]] = []
    for item in candidates:
        data.append(
            {
                "candidate_id": item.candidate_id,
                "name": item.restaurant.name,
                "location": item.restaurant.location,
                "cuisines": item.restaurant.cuisines,
                "cost": item.restaurant.cost,
                "rating": item.restaurant.rating,
                "score": item.score,
            }
        )
    return data
