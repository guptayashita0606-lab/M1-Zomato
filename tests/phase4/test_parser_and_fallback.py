from milestone1.phase4_llm import deterministic_fallback, enforce_grounding, parse_rankings_response


def test_parse_rankings_response_success() -> None:
    payload = {
        "rankings": [
            {"candidate_id": "cand_1", "rank": 1, "explanation": "Great cuisine fit."},
            {"candidate_id": "cand_2", "rank": 2, "explanation": "Good rating and budget."},
        ]
    }
    rankings = parse_rankings_response(payload)
    assert len(rankings) == 2
    assert rankings[0].candidate_id == "cand_1"


def test_enforce_grounding_filters_unknown_and_duplicates() -> None:
    payload = {
        "rankings": [
            {"candidate_id": "cand_2", "rank": 2, "explanation": "valid"},
            {"candidate_id": "cand_x", "rank": 1, "explanation": "invalid"},
            {"candidate_id": "cand_2", "rank": 3, "explanation": "duplicate"},
            {"candidate_id": "cand_1", "rank": 4, "explanation": "valid"},
        ]
    }
    parsed = parse_rankings_response(payload)
    grounded = enforce_grounding(parsed, allowed_candidate_ids={"cand_1", "cand_2"})
    assert [item.candidate_id for item in grounded] == ["cand_2", "cand_1"]


def test_deterministic_fallback_respects_top_k() -> None:
    candidates = [
        {"candidate_id": "cand_1", "name": "A", "rating": 4.3, "score": 11.0},
        {"candidate_id": "cand_2", "name": "B", "rating": 4.9, "score": 14.0},
        {"candidate_id": "cand_3", "name": "C", "rating": 4.0, "score": 10.0},
    ]
    fallback = deterministic_fallback(candidates, top_k=2)
    assert len(fallback) == 2
    assert fallback[0]["candidate_id"] == "cand_2"
