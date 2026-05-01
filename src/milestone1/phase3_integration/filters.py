from __future__ import annotations

from dataclasses import dataclass

from milestone1.phase1_ingestion import Restaurant
from milestone1.phase2_preferences import UserPreferences

_COST_SCORE = {"low": 1, "medium": 2, "high": 3, "unknown": 99}


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    restaurant: Restaurant
    score: float


def _budget_allowed(restaurant_cost: str, budget_band: str) -> bool:
    restaurant_score = _COST_SCORE.get(restaurant_cost, 99)
    budget_score = _COST_SCORE.get(budget_band, 99)
    return restaurant_score <= budget_score


def _cuisine_overlap_count(restaurant: Restaurant, preferred: list[str]) -> int:
    preferred_set = set(preferred)
    return len(preferred_set.intersection(set(restaurant.cuisines)))


def filter_and_rank(
    restaurants: list[Restaurant],
    preferences: UserPreferences,
    *,
    candidate_cap: int = 25,
) -> list[Candidate]:
    filtered: list[Candidate] = []
    for idx, restaurant in enumerate(restaurants):
        if restaurant.location != preferences.location:
            continue
        if restaurant.rating < preferences.minimum_rating:
            continue
        if not _budget_allowed(restaurant.cost, preferences.budget_band):
            continue
        overlap = _cuisine_overlap_count(restaurant, preferences.cuisines)
        if overlap == 0:
            continue

        # Simple deterministic composite: prioritize cuisine match then rating.
        score = overlap * 10.0 + restaurant.rating
        filtered.append(
            Candidate(
                candidate_id=f"cand_{idx}",
                restaurant=restaurant,
                score=score,
            )
        )

    filtered.sort(
        key=lambda c: (
            -c.score,
            -c.restaurant.rating,
            c.restaurant.cost,
            c.restaurant.name.lower(),
        )
    )
    return filtered[:candidate_cap]
