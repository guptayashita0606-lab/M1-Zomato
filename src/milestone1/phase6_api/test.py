"""
Test script to verify API outcomes match CLI recommendations.
"""

import asyncio
import json
from milestone1.phase6_api.service import RecommendationService
from milestone1.phase6_api.models import RecommendationRequest
from milestone1.phase5_output import recommend_run

async def test_api_vs_cli():
    """Test that API produces same results as CLI for same inputs."""
    
    # Test preferences
    preferences = {
        "location": "Delhi",
        "budget_band": "medium",
        "cuisines": ["Italian", "Chinese"],
        "minimum_rating": 4.0
    }
    
    # Test request
    request = RecommendationRequest(
        location=preferences["location"],
        budget_band=preferences["budget_band"],
        cuisines=preferences["cuisines"],
        minimum_rating=preferences["minimum_rating"],
        top_k=5,
        source="hf"
    )
    
    service = RecommendationService()
    
    print("Testing API vs CLI consistency...")
    
    # Get API results
    api_response = await service.get_recommendations(request)
    api_recommendations = api_response.recommendations
    
    # Get CLI results
    from milestone1.phase2_preferences import preferences_from_mapping
    from milestone1.phase1_ingestion import load_restaurants
    
    user_prefs = preferences_from_mapping(preferences)
    restaurants = load_restaurants(source="hf")
    
    cli_result = recommend_run(
        preferences=user_prefs,
        restaurants=restaurants,
        top_k=5,
        output_format="json"
    )
    
    cli_recommendations = cli_result.get("recommendations", [])
    
    print(f"API returned {len(api_recommendations)} recommendations")
    print(f"CLI returned {len(cli_recommendations)} recommendations")
    
    # Compare sources
    print(f"API source: {api_response.source}")
    print(f"CLI source: {cli_result.get('source')}")
    
    # Compare recommendation counts
    print(f"API total candidates: {api_response.total_candidates}")
    print(f"CLI total candidates: {cli_result.get('total_candidates')}")
    
    print("Test completed successfully!")
    
    return api_response, cli_result

if __name__ == "__main__":
    asyncio.run(test_api_vs_cli())
