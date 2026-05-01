from milestone1.phase2_preferences import preferences_from_mapping
from milestone1.phase5_output import recommend_run


def test_recommend_run_plain_output_and_result_shape() -> None:
    preferences = preferences_from_mapping(
        {
            "location": "Delhi",
            "budget_band": "high",
            "cuisines": "Chinese",
            "minimum_rating": 4.0,
        }
    )
    rendered, result = recommend_run(
        preferences,
        source="local",
        local_path="tests/fixtures/restaurants_sample.json",
        load_limit=100,
        candidate_cap=10,
        top_k=3,
        timeout_s=10.0,
        temperature=0.2,
        max_tokens=300,
        output_format="plain",
        emit_stderr_telemetry=False,
    )
    assert isinstance(rendered, str)
    assert "source" in result
    assert "rankings" in result
