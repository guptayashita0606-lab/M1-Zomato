from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ScopeInfo:
    product_slice: str
    stack: str
    secrets: List[str]
    supported_preference_fields: List[str]
    non_goals: List[str]


def get_scope_info() -> ScopeInfo:
    """Phase 0 scope assumptions for milestone 1."""
    return ScopeInfo(
        product_slice="Basic web UI is the source of user input and primary user surface; CLI is for diagnostics and local validation.",
        stack="Python 3.10+ package-first architecture. API/UI stack finalized in later phases.",
        secrets=["GROQ_API_KEY", "GROQ_MODEL (optional)"],
        supported_preference_fields=[
            "location",
            "budget_band",
            "cuisines",
            "minimum_rating",
            "additional_preferences",
        ],
        non_goals=[
            "User accounts and authentication",
            "Live Zomato API integration",
            "Maps/geospatial UI",
            "Production-grade deployment SLAs",
        ],
    )
