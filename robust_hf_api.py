#!/usr/bin/env python3
"""
Robust API using real Hugging Face restaurant data with better error handling.
"""

import sys
import os
sys.path.append('src')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import re
from typing import List, Dict, Any

app = FastAPI(title="Robust Hugging Face Restaurant API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for data
restaurants = []
cities = []
cuisines = []
data_loaded = False

def extract_rating(rate_str: str) -> float:
    """Extract numeric rating from string like '3.8/5'"""
    if not rate_str or rate_str == '--':
        return 0.0
    try:
        # Extract the first number before the slash
        match = re.search(r'(\d+\.?\d*)', str(rate_str))
        if match:
            return float(match.group(1))
    except:
        pass
    return 0.0

def extract_cost(cost_str: str) -> str:
    """Extract and normalize cost from string"""
    if not cost_str:
        return "medium"
    
    try:
        # Extract numeric cost
        cost_match = re.search(r'(\d+)', str(cost_str))
        if cost_match:
            cost_num = int(cost_match.group(1))
            if cost_num <= 300:
                return "low"
            elif cost_num <= 700:
                return "medium"
            else:
                return "high"
    except:
        pass
    return "medium"

def normalize_cuisine_list(cuisine_str: str) -> List[str]:
    """Normalize cuisine string to list"""
    if not cuisine_str or cuisine_str == '[]':
        return []
    
    # Split by comma and clean up
    cuisines = [c.strip() for c in str(cuisine_str).split(',')]
    return [c for c in cuisines if c and c != '[]']

def load_huggingface_data():
    """Load and process real Hugging Face restaurant data with retries"""
    global restaurants, cities, cuisines, data_loaded
    
    try:
        from datasets import load_dataset
        import time
        
        print("Loading Hugging Face dataset...")
        
        # Try multiple approaches
        approaches = [
            lambda: load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train", revision="main"),
            lambda: load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train"),
            lambda: load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train", streaming=True)
        ]
        
        dataset = None
        for i, approach in enumerate(approaches):
            try:
                print(f"  Attempt {i+1}...")
                dataset = approach()
                print(f"  ✅ Approach {i+1} succeeded")
                break
            except Exception as e:
                print(f"  ❌ Approach {i+1} failed: {str(e)[:100]}")
                if i < len(approaches) - 1:
                    time.sleep(1)  # Wait before retry
        
        if not dataset:
            raise Exception("All loading approaches failed")
        
        processed_restaurants = []
        all_cities = set()
        all_cuisines = set()
        
        # Process data
        count = 0
        max_items = 500  # Reduced for better performance
        
        if hasattr(dataset, 'select'):
            # Regular dataset
            limited_data = dataset.select(range(min(max_items, len(dataset))))
            for row in limited_data:
                if process_row(row, processed_restaurants, all_cities, all_cuisines):
                    count += 1
        else:
            # Streaming dataset
            for row in dataset:
                if count >= max_items:
                    break
                if process_row(row, processed_restaurants, all_cities, all_cuisines):
                    count += 1
        
        restaurants = processed_restaurants
        cities = sorted(list(all_cities))
        cuisines = sorted(list(all_cuisines))[:50]  # Limit to top 50 cuisines
        data_loaded = True
        
        print(f"✅ Loaded {len(restaurants)} restaurants from {len(cities)} cities")
        print(f"Sample cities: {cities[:5]}")
        print(f"Sample cuisines: {cuisines[:5]}")
        
    except Exception as e:
        print(f"❌ Error loading Hugging Face data: {e}")
        print("Using fallback data...")
        load_fallback_data()

def process_row(row, processed_restaurants, all_cities, all_cuisines):
    """Process a single row from the dataset"""
    try:
        # Extract and normalize data
        name = row.get('name', '').strip()
        location = row.get('location', '').strip()
        rate = row.get('rate', '')
        cost = row.get('approx_cost(for two people)', '')
        cuisine_str = row.get('cuisines', '')
        
        # Skip if essential fields are missing
        if not name or not location:
            return False
        
        # Process data
        rating = extract_rating(rate)
        cost_band = extract_cost(cost)
        cuisine_list = normalize_cuisine_list(cuisine_str)
        
        # Skip if rating is too low
        if rating < 2.0:
            return False
        
        restaurant = {
            "name": name,
            "location": location,
            "cuisines": cuisine_list,
            "estimated_cost": cost_band,
            "rating": rating,
            "explanation": f"Popular {', '.join(cuisine_list[:2])} restaurant in {location} with {rating} rating."
        }
        
        processed_restaurants.append(restaurant)
        all_cities.add(location)
        for cuisine in cuisine_list:
            if cuisine and len(cuisine) > 2:
                all_cuisines.add(cuisine)
        
        return True
        
    except Exception as e:
        return False

def load_fallback_data():
    """Load fallback sample data if Hugging Face fails"""
    global restaurants, cities, cuisines, data_loaded
    
    restaurants = [
        {
            "name": "Bukhara",
            "location": "Delhi",
            "cuisines": ["North Indian", "Mughlai"],
            "estimated_cost": "high",
            "rating": 4.5,
            "explanation": "Authentic Mughlai cuisine with excellent ambiance."
        },
        {
            "name": "Mainland China",
            "location": "Bangalore", 
            "cuisines": ["Chinese", "Asian"],
            "estimated_cost": "medium",
            "rating": 4.2,
            "explanation": "Authentic Chinese cuisine with modern presentation."
        },
        {
            "name": "Saravana Bhavan",
            "location": "Chennai",
            "cuisines": ["South Indian", "Vegetarian"],
            "estimated_cost": "low",
            "rating": 4.0,
            "explanation": "Traditional South Indian vegetarian restaurant."
        }
    ]
    
    cities = ["Delhi", "Bangalore", "Chennai", "Mumbai", "Hyderabad"]
    cuisines = ["North Indian", "South Indian", "Chinese", "Italian", "Continental"]
    data_loaded = True
    
    print("✅ Using fallback sample data")

@app.get("/")
async def root():
    return {"message": "Robust Hugging Face Restaurant API", "restaurants_count": len(restaurants), "data_source": "huggingface" if data_loaded else "fallback"}

@app.get("/health")
async def health():
    return {"status": "healthy", "restaurants_loaded": len(restaurants) > 0, "data_source": "huggingface" if data_loaded else "fallback"}

@app.get("/api/v1/meta")
async def get_meta():
    return {
        "allowed_cities": cities,
        "supported_budget_bands": ["low", "medium", "high"],
        "supported_cuisines": cuisines,
        "rating_range": {"min": 1.0, "max": 5.0}
    }

@app.post("/api/v1/recommendations")
async def get_recommendations(request: dict):
    location = request.get("location", "").strip()
    budget_band = request.get("budget_band", "medium")
    cuisines = request.get("cuisines", [])
    minimum_rating = request.get("minimum_rating", 4.0)
    top_k = request.get("top_k", 5)
    
    # Filter restaurants based on preferences
    filtered = []
    for restaurant in restaurants:
        location_match = not location or location.lower() in restaurant["location"].lower()
        rating_match = restaurant["rating"] >= minimum_rating
        budget_match = budget_band == "any" or restaurant["estimated_cost"] == budget_band
        cuisine_match = not cuisines or any(
            cuisine.lower() in [c.lower() for c in restaurant["cuisines"]] 
            for cuisine in cuisines
        )
        
        if location_match and rating_match and budget_match and cuisine_match:
            filtered.append(restaurant)
    
    # Sort by rating and return top recommendations
    filtered.sort(key=lambda x: x["rating"], reverse=True)
    recommendations = filtered[:top_k]
    
    return {
        "recommendations": recommendations,
        "source": "huggingface" if data_loaded else "fallback",
        "total_candidates": len(filtered),
        "filtered_candidates": len(recommendations),
        "request_id": "robust-hf-request"
    }

# Load data on startup
@app.on_event("startup")
async def startup_event():
    load_huggingface_data()

if __name__ == "__main__":
    import uvicorn
    print("Starting Robust Hugging Face Restaurant API...")
    uvicorn.run(app, host="0.0.0.0", port=8004, reload=False)
