import os

import pytest

from milestone1.phase1_ingestion import load_restaurants


pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    os.getenv("RUN_HF_INTEGRATION") != "1",
    reason="Set RUN_HF_INTEGRATION=1 to run Hugging Face ingestion tests.",
)
def test_hf_load_smoke() -> None:
    restaurants = load_restaurants(source="hf", limit=5)
    assert len(restaurants) > 0
    for restaurant in restaurants:
        assert restaurant.name
        assert restaurant.location
        assert restaurant.rating >= 0.0
