from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RankingItem:
    candidate_id: str
    rank: int
    explanation: str


class RankingParseError(ValueError):
    """Raised when LLM response does not match expected schema."""


def parse_rankings_response(payload: dict[str, Any]) -> list[RankingItem]:
    raw_rankings = payload.get("rankings")
    if not isinstance(raw_rankings, list):
        raise RankingParseError("Missing or invalid `rankings` list.")

    rankings: list[RankingItem] = []
    for raw in raw_rankings:
        if not isinstance(raw, dict):
            raise RankingParseError("Each ranking item must be an object.")
        candidate_id = raw.get("candidate_id")
        rank = raw.get("rank")
        explanation = raw.get("explanation")
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            raise RankingParseError("`candidate_id` must be non-empty string.")
        if not isinstance(rank, int) or rank <= 0:
            raise RankingParseError("`rank` must be positive integer.")
        if not isinstance(explanation, str) or not explanation.strip():
            raise RankingParseError("`explanation` must be non-empty string.")
        rankings.append(
            RankingItem(
                candidate_id=candidate_id.strip(),
                rank=rank,
                explanation=explanation.strip(),
            )
        )
    return rankings


def enforce_grounding(
    rankings: list[RankingItem], *, allowed_candidate_ids: set[str]
) -> list[RankingItem]:
    grounded: list[RankingItem] = []
    seen: set[str] = set()
    for item in sorted(rankings, key=lambda x: x.rank):
        if item.candidate_id not in allowed_candidate_ids:
            continue
        if item.candidate_id in seen:
            continue
        seen.add(item.candidate_id)
        grounded.append(item)
    return grounded
