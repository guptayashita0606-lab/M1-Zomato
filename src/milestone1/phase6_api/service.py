"""
Service layer for API business logic.
"""

import os
import uuid
import logging
import asyncio
from typing import Dict, Any, List
from concurrent.futures import TimeoutError as ConcurrentTimeoutError

from ..phase1_ingestion import load_restaurants
from ..phase2_preferences import preferences_from_mapping, allowed_cities_from_restaurants
from ..phase3_integration import filter_and_rank, build_prompt_payload, build_integration_output
from ..phase4_llm import recommend_with_groq
from ..phase5_output import recommend_run
from .models import RecommendationRequest, RecommendationResponse, RestaurantRecommendation

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service for handling recommendation requests."""
    
    def __init__(self):
        self._city_cache = None
    
    async def get_recommendations(self, request: RecommendationRequest) -> RecommendationResponse:
        """Generate restaurant recommendations based on user preferences."""
        request_id = str(uuid.uuid4())
        
        # Phase 4-aligned timeouts (30 seconds total)
        total_timeout = 30.0
        
        try:
            logger.info(f"Processing recommendation request {request_id}")
            
            # Parse preferences with timeout
            pref_mapping = {
                "location": request.location,
                "budget_band": request.budget_band,
                "cuisines": request.cuisines,
                "minimum_rating": request.minimum_rating
            }
            
            try:
                preferences = await asyncio.wait_for(
                    asyncio.to_thread(preferences_from_mapping, pref_mapping),
                    timeout=5.0
                )
            except asyncio.TimeoutError:
                logger.error(f"Preference parsing timeout for request {request_id}")
                raise Exception("Preference processing timeout")
            
            # Load restaurants with timeout
            try:
                if request.source == "local" and request.local_path:
                    restaurants = await asyncio.wait_for(
                        asyncio.to_thread(load_restaurants, source="local", local_path=request.local_path),
                        timeout=10.0
                    )
                else:
                    restaurants = await asyncio.wait_for(
                        asyncio.to_thread(load_restaurants, source="hf"),
                        timeout=15.0  # Longer timeout for Hugging Face
                    )
            except asyncio.TimeoutError:
                logger.error(f"Restaurant loading timeout for request {request_id}")
                raise Exception("Restaurant data loading timeout")
            
            # Generate recommendations using existing pipeline with timeout
            try:
                result = await asyncio.wait_for(
                    asyncio.to_thread(
                        recommend_run,
                        preferences=preferences,
                        restaurants=restaurants,
                        top_k=request.top_k or 5,
                        output_format="json"  # Use JSON for API
                    ),
                    timeout=10.0  # LLM timeout
                )
            except asyncio.TimeoutError:
                logger.error(f"Recommendation generation timeout for request {request_id}")
                raise Exception("Recommendation generation timeout")
            
            # Convert to API response format
            recommendations = []
            for rec in result.get("recommendations", []):
                recommendations.append(RestaurantRecommendation(
                    name=rec.get("name", ""),
                    cuisines=rec.get("cuisines", []),
                    rating=rec.get("rating", 0.0),
                    estimated_cost=rec.get("estimated_cost", ""),
                    explanation=rec.get("explanation", ""),
                    restaurant_id=rec.get("restaurant_id")
                ))
            
            logger.info(f"Successfully generated {len(recommendations)} recommendations for request {request_id}")
            
            return RecommendationResponse(
                recommendations=recommendations,
                source=result.get("source", "fallback"),
                total_candidates=result.get("total_candidates", 0),
                filtered_candidates=result.get("filtered_candidates", 0),
                request_id=request_id,
                telemetry=result.get("telemetry")
            )
            
        except Exception as e:
            logger.error(f"Error processing request {request_id}: {str(e)}")
            # Return empty recommendations on error
            return RecommendationResponse(
                recommendations=[],
                source="no_candidates",
                total_candidates=0,
                filtered_candidates=0,
                request_id=request_id,
                telemetry={"error": str(e), "error_type": type(e).__name__}
            )
    
    def get_allowed_cities(self) -> List[str]:
        """Get list of allowed cities from restaurant dataset."""
        if self._city_cache is None:
            restaurants = load_restaurants(source="hf")
            self._city_cache = allowed_cities_from_restaurants(restaurants)
        return self._city_cache
    
    def get_health_status(self) -> Dict[str, Any]:
        """Check health of dependencies."""
        status = {
            "groq_api": bool(os.getenv("GROQ_API_KEY")),
            "huggingface": True,  # Assume accessible unless error
            "database": True,  # In-memory dataset
            "city_cache": self._city_cache is not None
        }
        return status
