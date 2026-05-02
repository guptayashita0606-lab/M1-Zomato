#!/usr/bin/env python3
"""
Test Hugging Face integration.
"""

import requests
import json

def test_hf_api():
    base_url = "http://localhost:8004"
    
    print("Testing Hugging Face API integration...")
    
    # Test health
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health: {response.json()}")
    except Exception as e:
        print(f"❌ Health error: {e}")
    
    # Test meta
    try:
        response = requests.get(f"{base_url}/api/v1/meta")
        data = response.json()
        print(f"✅ Meta: {len(data['allowed_cities'])} cities, {len(data['supported_cuisines'])} cuisines")
        print(f"   Cities: {data['allowed_cities'][:5]}")
    except Exception as e:
        print(f"❌ Meta error: {e}")
    
    # Test recommendations
    try:
        test_request = {
            "location": "Bangalore",
            "cuisines": ["Chinese"],
            "minimum_rating": 4.0,
            "top_k": 3
        }
        response = requests.post(f"{base_url}/api/v1/recommendations", json=test_request)
        data = response.json()
        recommendations = data.get('recommendations', [])
        print(f"✅ Recommendations: {len(recommendations)} found")
        for i, rec in enumerate(recommendations):
            print(f"   {i+1}. {rec['name']} - {rec['location']} ({rec['rating']}★)")
    except Exception as e:
        print(f"❌ Recommendations error: {e}")

if __name__ == "__main__":
    test_hf_api()
