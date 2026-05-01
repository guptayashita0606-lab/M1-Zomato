"""
Phase 6 - Backend HTTP API

Provides FastAPI endpoints for restaurant recommendations.
Phase 6 owns server-side secrets, dataset access, and orchestration.
"""

from .app import create_app
from .models import RecommendationRequest, RecommendationResponse, HealthResponse

__all__ = ["create_app", "RecommendationRequest", "RecommendationResponse", "HealthResponse"]
