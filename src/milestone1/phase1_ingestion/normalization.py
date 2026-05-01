from __future__ import annotations

import re
from typing import Any


_NA_VALUES = {"", "na", "n/a", "none", "null", "-"}


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_name(value: Any) -> str:
    return _as_text(value)


def normalize_location(value: Any) -> str:
    text = _as_text(value)
    # Keep internal value deterministic for filtering.
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def normalize_cuisines(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        raw_items = value
    else:
        text = _as_text(value)
        if not text:
            return []
        raw_items = re.split(r"[,/|]", text)
    cuisines: list[str] = []
    seen: set[str] = set()
    for item in raw_items:
        token = re.sub(r"\s+", " ", _as_text(item)).lower()
        if not token or token in _NA_VALUES:
            continue
        if token not in seen:
            seen.add(token)
            cuisines.append(token)
    return cuisines


def normalize_rating(value: Any) -> float | None:
    text = _as_text(value).lower()
    if text in _NA_VALUES:
        return None
    match = re.search(r"\d+(\.\d+)?", text)
    if not match:
        return None
    try:
        rating = float(match.group(0))
    except ValueError:
        return None
    # Clamp to common 0..5 restaurant scale.
    return max(0.0, min(5.0, rating))


def normalize_cost(value: Any) -> str:
    text = _as_text(value).lower()
    if text in _NA_VALUES:
        return "unknown"

    # Extract first numeric amount if present.
    numeric_match = re.search(r"\d+", text.replace(",", ""))
    if numeric_match:
        amount = int(numeric_match.group(0))
        if amount <= 300:
            return "low"
        if amount <= 700:
            return "medium"
        return "high"

    alias_map = {
        "budget": "low",
        "cheap": "low",
        "affordable": "low",
        "moderate": "medium",
        "mid": "medium",
        "expensive": "high",
        "premium": "high",
        "luxury": "high",
    }
    for alias, band in alias_map.items():
        if alias in text:
            return band
    return "unknown"
