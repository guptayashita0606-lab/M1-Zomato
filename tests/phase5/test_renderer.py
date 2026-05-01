from milestone1.phase5_output import (
    NO_GROUNDED_PICKS_COPY,
    NO_MATCHES_COPY,
    render_markdown,
    render_plain,
)


def test_render_plain_rankings() -> None:
    result = {
        "source": "llm",
        "rankings": [
            {
                "rank": 1,
                "name": "Spice Hub",
                "cuisines": ["north indian", "chinese"],
                "rating": 4.2,
                "cost": "medium",
                "explanation": "Good fit.",
            }
        ],
    }
    text = render_plain(result)
    assert "1. Spice Hub" in text
    assert "Cuisine: north indian, chinese" in text


def test_render_markdown_no_candidates() -> None:
    text = render_markdown({"source": "no_candidates", "rankings": []})
    assert NO_MATCHES_COPY in text


def test_render_plain_no_grounded() -> None:
    text = render_plain({"source": "fallback", "rankings": []})
    assert text == NO_GROUNDED_PICKS_COPY
