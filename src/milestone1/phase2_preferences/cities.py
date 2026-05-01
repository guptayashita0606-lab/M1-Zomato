from __future__ import annotations

from typing import Iterable

from milestone1.phase1_ingestion import Restaurant


def allowed_cities_from_restaurants(restaurants: Iterable[Restaurant]) -> set[str]:
    return {restaurant.location.strip().lower() for restaurant in restaurants if restaurant.location}


def allowed_city_names(
    *,
    source: str = "hf",
    local_path: str | None = None,
    limit: int | None = 2000,
) -> set[str]:
    from milestone1.phase1_ingestion import load_restaurants

    restaurants = load_restaurants(source=source, local_path=local_path, limit=limit)
    return allowed_cities_from_restaurants(restaurants)
