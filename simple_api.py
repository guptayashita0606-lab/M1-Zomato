#!/usr/bin/env python3
"""
Simple test API to verify Hugging Face data connection.
"""

import sys
import os
sys.path.append('src')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from milestone1.phase1_ingestion import load_restaurants
from milestone1.phase2_preferences import allowed_cities_from_restaurants
import json

app = FastAPI(title="Simple Restaurant API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data on startup
restaurants = []
cities = []

@app.on_event("startup")
async def startup_event():
    global restaurants, cities
    print("Loading restaurants from Hugging Face...")
    try:
        restaurants = load_restaurants(source="hf", limit=100)  # Load first 100 for testing
        cities = allowed_cities_from_restaurants(restaurants)
        print(f"Loaded {len(restaurants)} restaurants from {len(cities)} cities")
        print(f"Sample cities: {cities[:5]}")
    except Exception as e:
        print(f"Error loading data: {e}")
        restaurants = []
        cities = []

@app.get("/")
async def root():
    return {"message": "Restaurant API is running", "restaurants_count": len(restaurants)}

@app.get("/health")
async def health():
    return {"status": "healthy", "restaurants_loaded": len(restaurants) > 0}

@app.get("/api/v1/meta")
async def get_meta():
    return {
        "allowed_cities": cities,
        "supported_budget_bands": ["low", "medium", "high"],
        "supported_cuisines": ["Italian", "Chinese", "Indian", "Mexican", "American", "Thai", "Japanese", "French"],
        "rating_range": {"min": 1.0, "max": 5.0}
    }

@app.post("/api/v1/recommendations")
async def get_recommendations(request: dict):
    location = request.get("location", "")
    budget_band = request.get("budget_band", "medium")
    cuisines = request.get("cuisines", [])
    minimum_rating = request.get("minimum_rating", 4.0)
    top_k = request.get("top_k", 5)
    
    # Filter restaurants based on preferences
    filtered = []
    for restaurant in restaurants:
        if location.lower() in restaurant.location.lower():
            if restaurant.rating >= minimum_rating:
                if not cuisines or any(cuisine in restaurant.cuisines for cuisine in cuisines):
                    filtered.append({
                        "name": restaurant.name,
                        "location": restaurant.location,
                        "cuisines": restaurant.cuisines,
                        "estimated_cost": restaurant.cost,
                        "rating": restaurant.rating,
                        "explanation": f"Great match for {location} with {restaurant.rating} rating and {', '.join(restaurant.cuisines[:3])} cuisine."
                    })
    
    # Return top recommendations
    recommendations = filtered[:top_k]
    
    return {
        "recommendations": recommendations,
        "source": "fallback",
        "total_candidates": len(filtered),
        "filtered_candidates": len(recommendations),
        "request_id": "test-request"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)
