from milestone1.phase1_ingestion.models import Restaurant
from milestone1.phase2_preferences.models import UserPreferences
from milestone1.phase3_integration import build_prompt_payload, filter_and_rank


def _restaurants() -> list[Restaurant]:
    return [
        Restaurant(
            name="A",
            location="delhi",
            cuisines=["italian", "chinese"],
            cost="medium",
            rating=4.5,
        ),
        Restaurant(
            name="B",
            location="delhi",
            cuisines=["north indian"],
            cost="low",
            rating=4.6,
        ),
        Restaurant(
            name="C",
            location="bangalore",
            cuisines=["italian"],
            cost="medium",
            rating=4.7,
        ),
        Restaurant(
            name="D",
            location="delhi",
            cuisines=["italian"],
            cost="high",
            rating=4.9,
        ),
    ]


def test_filter_and_rank_applies_hard_constraints() -> None:
    prefs = UserPreferences(
        location="delhi",
        budget_band="medium",
        cuisines=["italian"],
        minimum_rating=4.0,
        additional_preferences="",
    )
    candidates = filter_and_rank(_restaurants(), prefs, candidate_cap=10)
    assert len(candidates) == 1
    assert candidates[0].restaurant.name == "A"


def test_filter_and_rank_respects_candidate_cap() -> None:
    prefs = UserPreferences(
        location="delhi",
        budget_band="high",
        cuisines=["italian", "north indian"],
        minimum_rating=4.0,
        additional_preferences="",
    )
    candidates = filter_and_rank(_restaurants(), prefs, candidate_cap=2)
    assert len(candidates) == 2


def test_build_prompt_payload_contains_candidates_and_preferences() -> None:
    prefs = UserPreferences(
        location="delhi",
        budget_band="medium",
        cuisines=["italian"],
        minimum_rating=4.0,
        additional_preferences="quiet place",
    )
    candidates = filter_and_rank(_restaurants(), prefs, candidate_cap=10)
    payload = build_prompt_payload(prefs, candidates)
    assert "system_instructions" in payload
    assert payload["preferences"]["location"] == "delhi"
    assert len(payload["candidates"]) == 1
