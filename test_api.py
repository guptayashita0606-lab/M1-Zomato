#!/usr/bin/env python3
"""
Test script to verify API is working and returning data.
"""

import requests
import json

def test_api():
    base_url = "http://localhost:8001"
    
    print("Testing API endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health status: {response.status_code}")
        print(f"Health response: {response.json()}")
    except Exception as e:
        print(f"Health endpoint error: {e}")
    
    # Test meta endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/meta")
        print(f"Meta status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Cities available: {len(data.get('allowed_cities', []))}")
            print(f"Sample cities: {data.get('allowed_cities', [])[:5]}")
        else:
            print(f"Meta response: {response.text}")
    except Exception as e:
        print(f"Meta endpoint error: {e}")
    
    # Test recommendations endpoint
    try:
        test_request = {
            "location": "Delhi",
            "budget_band": "medium",
            "cuisines": ["Italian", "Chinese"],
            "minimum_rating": 4.0,
            "top_k": 3
        }
        response = requests.post(f"{base_url}/api/v1/recommendations", json=test_request)
        print(f"Recommendations status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('recommendations', [])
            print(f"Found {len(recommendations)} recommendations")
            for i, rec in enumerate(recommendations[:2]):
                print(f"  {i+1}. {rec.get('name', 'Unknown')} - {rec.get('location', 'Unknown')}")
        else:
            print(f"Recommendations response: {response.text}")
    except Exception as e:
        print(f"Recommendations endpoint error: {e}")

if __name__ == "__main__":
    test_api()
