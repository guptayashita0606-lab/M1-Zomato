import pytest

from milestone1.phase2_preferences import PreferencesValidationError, preferences_from_mapping


def test_preferences_parse_success() -> None:
    prefs = preferences_from_mapping(
        {
            "location": "Delhi",
            "budget_band": "mid",
            "cuisines": "Italian, Chinese",
            "minimum_rating": "4.2",
            "additional_preferences": "family friendly",
        }
    )
    assert prefs.location == "delhi"
    assert prefs.budget_band == "medium"
    assert prefs.cuisines == ["italian", "chinese"]
    assert prefs.minimum_rating == 4.2


def test_preferences_parse_unknown_city_rejected() -> None:
    with pytest.raises(PreferencesValidationError):
        preferences_from_mapping(
            {
                "location": "unknowncity",
                "budget_band": "low",
                "cuisines": "italian",
                "minimum_rating": "4",
            },
            allowed_city_names={"delhi", "bangalore"},
        )


def test_preferences_parse_invalid_rating_rejected() -> None:
    with pytest.raises(PreferencesValidationError):
        preferences_from_mapping(
            {
                "location": "delhi",
                "budget_band": "low",
                "cuisines": "italian",
                "minimum_rating": "8",
            }
        )


def test_preferences_parse_missing_cuisine_rejected() -> None:
    with pytest.raises(PreferencesValidationError):
        preferences_from_mapping(
            {
                "location": "delhi",
                "budget_band": "high",
                "cuisines": "",
                "minimum_rating": "4",
            }
        )
