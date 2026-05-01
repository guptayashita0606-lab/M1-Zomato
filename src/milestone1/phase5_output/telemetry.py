from __future__ import annotations

import json
import sys
from typing import Any


def emit_telemetry(
    *,
    source: str,
    latency_ms: float,
    candidate_count: int,
    ranking_count: int,
) -> None:
    payload: dict[str, Any] = {
        "event": "recommend_run",
        "source": source,
        "latency_ms": round(latency_ms, 2),
        "candidate_count": candidate_count,
        "ranking_count": ranking_count,
    }
    print(json.dumps(payload), file=sys.stderr)
