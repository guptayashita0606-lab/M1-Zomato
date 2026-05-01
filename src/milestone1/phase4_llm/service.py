from __future__ import annotations

from typing import Any

from milestone1.phase2_preferences import UserPreferences
from milestone1.phase3_integration import build_integration_output

from .client import GroqClient, GroqClientError
from .fallback import deterministic_fallback
from .parser import RankingParseError, enforce_grounding, parse_rankings_response


def recommend_with_groq(
    preferences: UserPreferences,
    *,
    source: str = "hf",
    local_path: str | None = None,
    load_limit: int | None = 2000,
    candidate_cap: int = 25,
    top_k: int = 5,
    timeout_s: float = 30.0,
    temperature: float = 0.2,
    max_tokens: int = 700,
) -> dict[str, Any]:
    integration = build_integration_output(
        preferences,
        source=source,
        local_path=local_path,
        load_limit=load_limit,
        candidate_cap=candidate_cap,
    )
    candidates: list[dict[str, Any]] = integration["candidates"]
    if not candidates:
        return {
            "source": "no_candidates",
            "rankings": [],
            "candidate_count": 0,
            "error": None,
        }

    prompt_payload = integration["prompt_payload"]
    allowed_ids = {c["candidate_id"] for c in candidates}
    try:
        client = GroqClient(
            timeout_s=timeout_s,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        raw_response = client.chat_json(
            system_instructions=prompt_payload["system_instructions"],
            user_prompt=prompt_payload["user_prompt"],
        )
        parsed = parse_rankings_response(raw_response)
        grounded = enforce_grounding(parsed, allowed_candidate_ids=allowed_ids)
        if not grounded:
            raise RankingParseError("No grounded rankings produced by model.")

        index = {c["candidate_id"]: c for c in candidates}
        rankings: list[dict[str, Any]] = []
        for idx, item in enumerate(grounded[:top_k], start=1):
            candidate = index[item.candidate_id]
            rankings.append(
                {
                    "candidate_id": item.candidate_id,
                    "rank": idx,
                    "explanation": item.explanation,
                    "name": candidate["name"],
                    "location": candidate["location"],
                    "cuisines": candidate["cuisines"],
                    "cost": candidate["cost"],
                    "rating": candidate["rating"],
                }
            )
        return {
            "source": "llm",
            "rankings": rankings,
            "candidate_count": len(candidates),
            "error": None,
        }
    except (GroqClientError, RankingParseError, KeyError, TypeError, ValueError) as exc:
        fallback_rankings = deterministic_fallback(candidates, top_k=top_k)
        index = {c["candidate_id"]: c for c in candidates}
        rankings: list[dict[str, Any]] = []
        for item in fallback_rankings:
            candidate = index[item["candidate_id"]]
            rankings.append(
                {
                    **item,
                    "name": candidate["name"],
                    "location": candidate["location"],
                    "cuisines": candidate["cuisines"],
                    "cost": candidate["cost"],
                    "rating": candidate["rating"],
                }
            )
        return {
            "source": "fallback",
            "rankings": rankings,
            "candidate_count": len(candidates),
            "error": str(exc),
        }
