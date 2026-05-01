from __future__ import annotations

from dataclasses import dataclass


VALID_BUDGET_BANDS = {"low", "medium", "high"}
_BUDGET_ALIASES = {
    "budget": "low",
    "cheap": "low",
    "affordable": "low",
    "mid": "medium",
    "moderate": "medium",
    "expensive": "high",
    "premium": "high",
    "luxury": "high",
}


@dataclass(frozen=True)
class FieldError:
    field: str
    message: str


class PreferencesValidationError(ValueError):
    def __init__(self, errors: list[FieldError]) -> None:
        self.errors = errors
        message = "; ".join(f"{error.field}: {error.message}" for error in errors)
        super().__init__(message)


def normalize_text(value: object) -> str:
    return str(value or "").strip().lower()


def normalize_budget_band(value: object) -> str:
    text = normalize_text(value)
    if text in VALID_BUDGET_BANDS:
        return text
    return _BUDGET_ALIASES.get(text, text)


def normalize_rating(value: object) -> float | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        parsed = float(text)
    except (TypeError, ValueError):
        return None
    if parsed < 0.0 or parsed > 5.0:
        return None
    return parsed


def normalize_cuisines(value: object) -> list[str]:
    text = str(value or "").strip().lower()
    if not text:
        return []
    raw = text.replace("/", ",")
    tokens = [token.strip() for token in raw.split(",")]
    cuisines: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        if not token:
            continue
        if token not in seen:
            seen.add(token)
            cuisines.append(token)
    return cuisines
