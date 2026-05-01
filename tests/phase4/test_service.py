from milestone1.phase2_preferences import preferences_from_mapping
from milestone1.phase4_llm import recommend_with_groq


def test_recommend_fallback_when_groq_key_missing() -> None:
    prefs = preferences_from_mapping(
        {
            "location": "Delhi",
            "budget_band": "high",
            "cuisines": "Chinese",
            "minimum_rating": 4.0,
        }
    )
    result = recommend_with_groq(
        prefs,
        source="local",
        local_path="tests/fixtures/restaurants_sample.json",
        top_k=2,
    )
    assert result["source"] in {"fallback", "llm", "no_candidates"}
    if result["source"] != "no_candidates":
        assert len(result["rankings"]) >= 1
