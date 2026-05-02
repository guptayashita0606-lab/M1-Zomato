#!/usr/bin/env python3
"""
Test Hugging Face recommendations with correct locations.
"""

import requests
import json

def test_recommendations():
    base_url = "http://localhost:8004"
    
    print("Testing Hugging Face recommendations...")
    
    # Test with available locations
    test_requests = [
        {"location": "Basavanagudi", "cuisines": ["North Indian"], "minimum_rating": 3.5},
        {"location": "Banashankari", "cuisines": ["Chinese"], "minimum_rating": 4.0},
        {"location": "", "cuisines": ["North Indian"], "minimum_rating": 4.0},  # Empty location
        {"location": "Basavanagudi", "cuisines": [], "minimum_rating": 3.0},  # Empty cuisines
    ]
    
    for i, request in enumerate(test_requests):
        print(f"\nTest {i+1}: {request}")
        try:
            response = requests.post(f"{base_url}/api/v1/recommendations", json=request)
            data = response.json()
            recommendations = data.get('recommendations', [])
            print(f"✅ Found {len(recommendations)} recommendations")
            
            for j, rec in enumerate(recommendations[:2]):
                print(f"   {j+1}. {rec['name']} - {rec['location']} ({rec['rating']}★)")
                print(f"      Cuisines: {', '.join(rec['cuisines'][:3])}")
                print(f"      Cost: {rec['estimated_cost']}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_recommendations()
