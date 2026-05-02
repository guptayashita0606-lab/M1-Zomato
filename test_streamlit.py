#!/usr/bin/env python3
"""
Test Streamlit application functionality.
"""

import requests
import time

def test_streamlit_app():
    """Test if Streamlit app is running and accessible."""
    
    print("Testing Streamlit Application...")
    
    # Test 1: Check if Streamlit is running
    try:
        response = requests.get("http://localhost:8502", timeout=5)
        if response.status_code == 200:
            print("✅ Streamlit app is running on http://localhost:8502")
        else:
            print(f"❌ Streamlit app returned status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Streamlit app is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Error connecting to Streamlit: {e}")
        return False
    
    # Test 2: Check if backend API is accessible from Streamlit
    try:
        response = requests.get("http://localhost:8004/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is accessible")
            data = response.json()
            print(f"   Backend status: {data.get('status', 'unknown')}")
            print(f"   Restaurants loaded: {data.get('restaurants_loaded', False)}")
        else:
            print(f"❌ Backend API returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
    
    # Test 3: Test Streamlit app components
    print("\nTesting Streamlit app components...")
    
    # Test if the app can load metadata
    try:
        response = requests.get("http://localhost:8004/api/v1/meta", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Metadata loaded: {len(data.get('allowed_cities', []))} cities, {len(data.get('supported_cuisines', []))} cuisines")
        else:
            print(f"❌ Metadata API error: {response.status_code}")
    except Exception as e:
        print(f"❌ Metadata loading error: {e}")
    
    return True

if __name__ == "__main__":
    test_streamlit_app()
