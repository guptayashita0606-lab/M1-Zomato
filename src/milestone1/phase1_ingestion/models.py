from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Restaurant:
    """Canonical restaurant schema used across milestone phases."""

    name: str
    location: str
    cuisines: list[str]
    cost: str
    rating: float
    metadata: dict[str, Any] = field(default_factory=dict)
