"""
Pydantic models for API request/response schemas.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    """Request model for restaurant recommendations."""
    location: str = Field(..., min_length=1, max_length=100, description="City or area name")
    budget_band: Literal["low", "medium", "high"] = Field(..., description="Budget preference")
    cuisines: List[str] = Field(..., min_items=1, max_items=10, description="List of preferred cuisines")
    minimum_rating: float = Field(ge=1.0, le=5.0, description="Minimum rating threshold")
    top_k: Optional[int] = Field(default=5, ge=1, le=20, description="Number of recommendations to return")
    source: Optional[Literal["local", "hf"]] = Field(default="hf", description="Data source")
    local_path: Optional[str] = Field(None, max_length=500, description="Path to local dataset (if source=local)")
    
    class Config:
        # Add request size validation
        max_request_size = 10 * 1024  # 10KB limit


class RestaurantRecommendation(BaseModel):
    """Individual restaurant recommendation."""
    name: str
    cuisines: List[str]
    rating: float
    estimated_cost: str
    explanation: str
    restaurant_id: Optional[str] = None


class RecommendationResponse(BaseModel):
    """Response model for restaurant recommendations."""
    recommendations: List[RestaurantRecommendation]
    source: Literal["llm", "fallback", "no_candidates"]
    total_candidates: int
    filtered_candidates: int
    request_id: Optional[str] = None
    telemetry: Optional[dict] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "0.1.0"
    dependencies: dict


class MetaResponse(BaseModel):
    """Metadata response with allowed cities."""
    allowed_cities: List[str]
    supported_budget_bands: List[str]
    supported_cuisines: List[str]
    rating_range: dict
