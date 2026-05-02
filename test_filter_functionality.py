#!/usr/bin/env python3
"""
Test complete filter functionality end-to-end.
"""

import requests
import json

def test_filter_functionality():
    frontend_url = "http://localhost:3000"
    backend_url = "http://localhost:8004"
    
    print("Testing Filter Functionality End-to-End...")
    
    # Test 1: Check frontend proxy to backend
    print("\n1. Testing frontend proxy connection...")
    try:
        response = requests.get(f"{frontend_url}/api/v1/meta")
        print(f"✅ Frontend proxy status: {response.status_code}")
        meta_data = response.json()
        print(f"   Cities available: {len(meta_data['allowed_cities'])}")
        print(f"   Cuisines available: {len(meta_data['supported_cuisines'])}")
    except Exception as e:
        print(f"❌ Frontend proxy error: {e}")
    
    # Test 2: Test different filter combinations
    print("\n2. Testing filter combinations...")
    
    test_cases = [
        {
            "name": "Location + Cuisine + Rating",
            "request": {
                "location": "Basavanagudi",
                "budget_band": "medium",
                "cuisines": ["North Indian"],
                "minimum_rating": 4.0,
                "top_k": 5
            }
        },
        {
            "name": "Location only",
            "request": {
                "location": "Banashankari",
                "budget_band": "medium",
                "cuisines": [],
                "minimum_rating": 3.0,
                "top_k": 5
            }
        },
        {
            "name": "Cuisine only",
            "request": {
                "location": "",
                "budget_band": "medium",
                "cuisines": ["Chinese"],
                "minimum_rating": 3.5,
                "top_k": 5
            }
        },
        {
            "name": "High rating filter",
            "request": {
                "location": "",
                "budget_band": "medium",
                "cuisines": ["North Indian"],
                "minimum_rating": 4.5,
                "top_k": 5
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n   Test {i+1}: {test_case['name']}")
        try:
            # Test via frontend proxy
            response = requests.post(f"{frontend_url}/api/v1/recommendations", json=test_case['request'])
            data = response.json()
            recommendations = data.get('recommendations', [])
            print(f"   ✅ Frontend: {len(recommendations)} recommendations")
            
            # Test direct backend
            response = requests.post(f"{backend_url}/api/v1/recommendations", json=test_case['request'])
            data = response.json()
            recommendations = data.get('recommendations', [])
            print(f"   ✅ Backend: {len(recommendations)} recommendations")
            
            # Show sample results
            if recommendations:
                rec = recommendations[0]
                print(f"      Sample: {rec['name']} - {rec['location']} ({rec['rating']}★)")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test 3: Test form validation requirements
    print("\n3. Testing form validation scenarios...")
    
    validation_tests = [
        {
            "name": "Empty location",
            "request": {
                "location": "",
                "budget_band": "medium",
                "cuisines": ["North Indian"],
                "minimum_rating": 4.0,
                "top_k": 5
            }
        },
        {
            "name": "Empty cuisines",
            "request": {
                "location": "Basavanagudi",
                "budget_band": "medium",
                "cuisines": [],
                "minimum_rating": 4.0,
                "top_k": 5
            }
        }
    ]
    
    for test in validation_tests:
        print(f"\n   {test['name']}:")
        try:
            response = requests.post(f"{backend_url}/api/v1/recommendations", json=test['request'])
            data = response.json()
            recommendations = data.get('recommendations', [])
            print(f"   ✅ Backend accepts: {len(recommendations)} recommendations")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_filter_functionality()
