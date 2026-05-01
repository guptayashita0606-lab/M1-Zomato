from __future__ import annotations

from typing import Any


NO_MATCHES_COPY = (
    "No restaurants matched your filters. Try relaxing location, cuisine, rating, or budget."
)
NO_GROUNDED_PICKS_COPY = (
    "The model could not justify grounded picks right now. Try again or adjust preferences."
)


def render_markdown(result: dict[str, Any]) -> str:
    source = result.get("source", "unknown")
    rankings = result.get("rankings", [])
    if not rankings:
        if source == "no_candidates":
            return f"## Recommendations\n\n{NO_MATCHES_COPY}"
        return f"## Recommendations\n\n{NO_GROUNDED_PICKS_COPY}"

    lines: list[str] = ["## Top Recommendations"]
    for item in rankings:
        cuisines = ", ".join(item.get("cuisines", []))
        lines.extend(
            [
                "",
                f"### {item.get('rank', '-')}. {item.get('name', 'Unknown')}",
                f"- Cuisine: {cuisines or 'N/A'}",
                f"- Rating: {item.get('rating', 'N/A')}",
                f"- Estimated Cost: {item.get('cost', 'N/A')}",
                f"- Why recommended: {item.get('explanation', 'N/A')}",
            ]
        )
    return "\n".join(lines)


def render_plain(result: dict[str, Any]) -> str:
    source = result.get("source", "unknown")
    rankings = result.get("rankings", [])
    if not rankings:
        if source == "no_candidates":
            return NO_MATCHES_COPY
        return NO_GROUNDED_PICKS_COPY

    lines: list[str] = []
    for item in rankings:
        cuisines = ", ".join(item.get("cuisines", []))
        lines.extend(
            [
                f"{item.get('rank', '-')}. {item.get('name', 'Unknown')}",
                f"   Cuisine: {cuisines or 'N/A'}",
                f"   Rating: {item.get('rating', 'N/A')}",
                f"   Estimated Cost: {item.get('cost', 'N/A')}",
                f"   Why: {item.get('explanation', 'N/A')}",
            ]
        )
    return "\n".join(lines)
