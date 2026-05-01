from __future__ import annotations

from typing import Any


def deterministic_fallback(
    candidates: list[dict[str, Any]], *, top_k: int = 5
) -> list[dict[str, Any]]:
    ordered = sorted(
        candidates,
        key=lambda c: (
            -float(c.get("score", 0.0)),
            -float(c.get("rating", 0.0)),
            str(c.get("name", "")).lower(),
        ),
    )
    picks: list[dict[str, Any]] = []
    for idx, candidate in enumerate(ordered[:top_k], start=1):
        picks.append(
            {
                "candidate_id": candidate["candidate_id"],
                "rank": idx,
                "explanation": (
                    f"{candidate.get('name', 'This restaurant')} matches your core filters "
                    "and ranks strongly by rating and cuisine overlap."
                ),
            }
        )
    return picks
