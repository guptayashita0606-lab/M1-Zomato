from __future__ import annotations

from time import perf_counter
from typing import Any

from milestone1.phase2_preferences import UserPreferences
from milestone1.phase4_llm import recommend_with_groq

from .renderer import render_markdown, render_plain
from .telemetry import emit_telemetry


def recommend_run(
    preferences: UserPreferences,
    *,
    source: str,
    local_path: str | None,
    load_limit: int,
    candidate_cap: int,
    top_k: int,
    timeout_s: float,
    temperature: float,
    max_tokens: int,
    output_format: str = "plain",
    emit_stderr_telemetry: bool = True,
) -> tuple[str, dict[str, Any]]:
    start = perf_counter()
    result = recommend_with_groq(
        preferences,
        source=source,
        local_path=local_path,
        load_limit=load_limit,
        candidate_cap=candidate_cap,
        top_k=top_k,
        timeout_s=timeout_s,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    latency_ms = (perf_counter() - start) * 1000

    if emit_stderr_telemetry:
        emit_telemetry(
            source=result.get("source", "unknown"),
            latency_ms=latency_ms,
            candidate_count=int(result.get("candidate_count", 0)),
            ranking_count=len(result.get("rankings", [])),
        )

    if output_format == "markdown":
        return render_markdown(result), result
    return render_plain(result), result
