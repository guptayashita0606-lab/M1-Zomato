#!/usr/bin/env python3
"""
Debug script to identify Streamlit deployment issues.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all required imports work."""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        from datasets import load_dataset
        print("✅ datasets imported successfully")
    except ImportError as e:
        print(f"⚠️ datasets import failed: {e}")
        print("   This is okay - app will use sample data")
    
    try:
        from milestone1.phase8_streamlit.standalone_app import main
        print("✅ standalone_app imported successfully")
    except ImportError as e:
        print(f"❌ standalone_app import failed: {e}")
        return False
    
    return True

def test_theme():
    """Test theme configuration."""
    print("\nTesting theme...")
    
    try:
        from milestone1.phase8_streamlit.theme import get_theme_config, get_custom_css
        theme = get_theme_config()
        css = get_custom_css()
        print(f"✅ Theme loaded: {theme.get('theme', {}).get('primaryColor', 'N/A')}")
        print(f"✅ CSS loaded: {len(css)} characters")
        return True
    except Exception as e:
        print(f"❌ Theme test failed: {e}")
        return False

def test_data_loading():
    """Test data loading functionality."""
    print("\nTesting data loading...")
    
    try:
        from milestone1.phase8_streamlit.standalone_app import load_restaurant_data
        restaurants, cities, cuisines = load_restaurant_data()
        print(f"✅ Data loaded: {len(restaurants)} restaurants, {len(cities)} cities, {len(cuisines)} cuisines")
        return True
    except Exception as e:
        print(f"❌ Data loading test failed: {e}")
        return False

def main():
    """Run all debug tests."""
    print("=== Streamlit Debug Tests ===")
    
    tests = [
        ("Import Test", test_imports),
        ("Theme Test", test_theme),
        ("Data Loading Test", test_data_loading)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n=== Summary ===")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'✅ All tests passed' if all_passed else '❌ Some tests failed'}")
    
    return all_passed

if __name__ == "__main__":
    main()
