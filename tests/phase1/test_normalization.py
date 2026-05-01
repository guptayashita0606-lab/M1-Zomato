from milestone1.phase1_ingestion.loader import load_restaurants
from milestone1.phase1_ingestion.normalization import (
    normalize_cost,
    normalize_cuisines,
    normalize_location,
    normalize_rating,
)
from milestone1.phase1_ingestion.schema import SchemaAssertionError, assert_source_schema


def test_normalize_rating_text_and_bounds() -> None:
    assert normalize_rating("4.2/5") == 4.2
    assert normalize_rating("6.8") == 5.0
    assert normalize_rating("n/a") is None


def test_normalize_cuisines_dedupes_and_cleans() -> None:
    assert normalize_cuisines("Italian, chinese / Italian") == ["italian", "chinese"]


def test_normalize_cost_numeric_bands() -> None:
    assert normalize_cost("250") == "low"
    assert normalize_cost("500") == "medium"
    assert normalize_cost("1500") == "high"


def test_normalize_location_lowercase() -> None:
    assert normalize_location("  New   Delhi ") == "new delhi"


def test_schema_assertion_missing_field_raises() -> None:
    row = {"restaurant_name": "A", "location": "X", "cuisines": "Italian", "cost": 300}
    try:
        assert_source_schema(row)
        assert False, "Expected SchemaAssertionError"
    except SchemaAssertionError:
        pass


def test_load_restaurants_local_json(tmp_path) -> None:
    sample_file = tmp_path / "restaurants.json"
    sample_file.write_text(
        '[{"restaurant_name":"R1","location":"Delhi","cuisines":"North Indian","average_cost_for_two":"300","aggregate_rating":"4.1"},'
        '{"restaurant_name":"R1","location":"Delhi","cuisines":"North Indian","average_cost_for_two":"300","aggregate_rating":"4.1"},'
        '{"restaurant_name":"R2","location":"Bangalore","cuisines":"Italian,Chinese","average_cost_for_two":"900","aggregate_rating":"4.7"}]',
        encoding="utf-8",
    )
    restaurants = load_restaurants(source="local", local_path=str(sample_file), limit=10)
    assert len(restaurants) == 2
    assert restaurants[0].location == "delhi"
    assert restaurants[1].cost == "high"
