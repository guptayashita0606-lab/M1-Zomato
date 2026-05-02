#!/usr/bin/env python3
"""
Test standalone Streamlit application functionality.
"""

import requests
import time

def test_standalone_streamlit():
    """Test if standalone Streamlit app is running and accessible."""
    
    print("Testing Standalone Streamlit Application...")
    
    # Test 1: Check if Streamlit is running
    try:
        response = requests.get("http://localhost:8503", timeout=5)
        if response.status_code == 200:
            print("✅ Standalone Streamlit app is running on http://localhost:8503")
        else:
            print(f"❌ Streamlit app returned status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Streamlit app is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Error connecting to Streamlit: {e}")
        return False
    
    print("✅ Standalone Streamlit app is ready for deployment")
    return True

if __name__ == "__main__":
    test_standalone_streamlit()
