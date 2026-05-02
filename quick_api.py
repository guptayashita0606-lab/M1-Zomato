#!/usr/bin/env python3
"""
Quick API with sample data to test frontend immediately.
"""

import sys
sys.path.append('src')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(title="Quick Restaurant API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample restaurant data (mimicking Hugging Face structure)
sample_restaurants = [
    {
        "name": "Bukhara",
        "location": "Delhi",
        "cuisines": ["North Indian", "Mughlai", "Kebab"],
        "estimated_cost": "medium",
        "rating": 4.5,
        "explanation": "Authentic Mughlai cuisine with excellent ambiance and service. Perfect for traditional Indian dining experience."
    },
    {
        "name": "Dominos Pizza",
        "location": "Mumbai",
        "cuisines": ["Pizza", "Fast Food", "Italian"],
        "estimated_cost": "low",
        "rating": 3.8,
        "explanation": "Popular pizza chain with quick delivery and consistent quality. Great for casual dining."
    },
    {
        "name": "Mainland China",
        "location": "Bangalore",
        "cuisines": ["Chinese", "Asian", "Sichuan"],
        "estimated_cost": "medium",
        "rating": 4.2,
        "explanation": "Authentic Chinese cuisine with modern presentation. Known for excellent dim sum and stir-fry dishes."
    },
    {
        "name": "Saravana Bhavan",
        "location": "Chennai",
        "cuisines": ["South Indian", "Vegetarian", "Dosas"],
        "estimated_cost": "low",
        "rating": 4.0,
        "explanation": "Traditional South Indian vegetarian restaurant. Famous for authentic dosas and filter coffee."
    },
    {
        "name": "Leopold Cafe",
        "location": "Mumbai",
        "cuisines": ["Continental", "Cafe", "Multi-cuisine"],
        "estimated_cost": "medium",
        "rating": 4.3,
        "explanation": "Trendy cafe with colonial ambiance. Great for casual meetings and European cuisine."
    }
]

available_cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Jaipur"]
available_cuisines = ["North Indian", "South Indian", "Chinese", "Italian", "Continental", "Mughlai", "Pizza", "Cafe", "Multi-cuisine", "Vegetarian"]

@app.get("/")
async def root():
    return {"message": "Quick Restaurant API", "restaurants_count": len(sample_restaurants)}

@app.get("/health")
async def health():
    return {"status": "healthy", "restaurants_loaded": True}

@app.get("/api/v1/meta")
async def get_meta():
    return {
        "allowed_cities": available_cities,
        "supported_budget_bands": ["low", "medium", "high"],
        "supported_cuisines": available_cuisines,
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
    for restaurant in sample_restaurants:
        location_match = location.lower() in restaurant["location"].lower() or location.strip() == ""
        rating_match = restaurant["rating"] >= minimum_rating
        cuisine_match = not cuisines or any(cuisine.lower() in [c.lower() for c in restaurant["cuisines"]] for cuisine in cuisines)
        
        if location_match and rating_match and cuisine_match:
            filtered.append(restaurant)
    
    # Return top recommendations
    recommendations = filtered[:top_k] if filtered else sample_restaurants[:top_k]
    
    return {
        "recommendations": recommendations,
        "source": "sample_data",
        "total_candidates": len(filtered),
        "filtered_candidates": len(recommendations),
        "request_id": "quick-test-request"
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Quick API with sample restaurant data...")
    print(f"Loaded {len(sample_restaurants)} sample restaurants")
    print(f"Available cities: {available_cities}")
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=False)
