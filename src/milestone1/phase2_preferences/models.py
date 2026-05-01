from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UserPreferences:
    location: str
    budget_band: str
    cuisines: list[str]
    minimum_rating: float
    additional_preferences: str = ""
