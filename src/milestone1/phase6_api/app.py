"""
FastAPI application for restaurant recommendation API.
"""

import os
import logging
import json
from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from .service import RecommendationService
from .models import RecommendationRequest, RecommendationResponse, HealthResponse, MetaResponse


# Global service instance
recommendation_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    global recommendation_service
    recommendation_service = RecommendationService()
    yield
    # Cleanup if needed


# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    # Development-only CORS allowlist
    allowed_origins = ["http://localhost:3000", "http://localhost:5173"]
    if os.getenv("ENVIRONMENT") == "development":
        allowed_origins.extend(["http://127.0.0.1:3000", "http://127.0.0.1:5173"])
    
    app = FastAPI(
        title="Restaurant Recommendation API",
        description="AI-powered restaurant recommendation system",
        version="0.1.0",
        lifespan=lifespan
    )
    
    # Add CORS middleware with development allowlist
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],  # Restrict to needed methods
        allow_headers=["*"],
    )
    
    # Add request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url}")
        
        response = await call_next(request)
        
        # Log response with timing
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
        
        return response
    
    return app


# Create app instance
app = create_app()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    if not recommendation_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not initialized"
        )
    
    dependencies = recommendation_service.get_health_status()
    
    return HealthResponse(
        status="healthy" if all(dependencies.values()) else "degraded",
        version="0.1.0",
        dependencies=dependencies
    )


@app.get("/api/v1/meta", response_model=MetaResponse)
async def get_metadata():
    """Get metadata about supported options."""
    if not recommendation_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not initialized"
        )
    
    allowed_cities = recommendation_service.get_allowed_cities()
    
    return MetaResponse(
        allowed_cities=allowed_cities,
        supported_budget_bands=["low", "medium", "high"],
        supported_cuisines=[
            "North Indian", "South Indian", "Chinese", "Italian", "Mexican",
            "Thai", "Japanese", "Continental", "Fast Food", "Cafe",
            "Bakery", "Desserts", "Beverages", "Street Food"
        ],
        rating_range={"min": 1.0, "max": 5.0}
    )


@app.post("/api/v1/recommendations", response_model=RecommendationResponse)
async def create_recommendations(request: RecommendationRequest):
    """Generate restaurant recommendations based on user preferences."""
    if not recommendation_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not initialized"
        )
    
    try:
        logger.info(f"Received recommendation request: location={request.location}, budget={request.budget_band}")
        response = await recommendation_service.get_recommendations(request)
        logger.info(f"Generated {len(response.recommendations)} recommendations")
        return response
    except Exception as e:
        logger.error(f"Failed to generate recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with JSON responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error", "status_code": 500}
    )
