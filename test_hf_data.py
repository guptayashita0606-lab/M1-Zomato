#!/usr/bin/env python3
"""
Test script to debug Hugging Face data loading
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

print("🔍 Testing Hugging Face data loading...")

try:
    from milestone1.phase1_ingestion.loader import iter_restaurants
    print("✅ Import successful")
    
    # Test loading data
    restaurants = list(iter_restaurants(source='hf', limit=10))
    print(f"📊 Loaded {len(restaurants)} restaurants from Hugging Face")
    
    # Show sample data
    for i, r in enumerate(restaurants[:5]):
        print(f"  {i+1}. {r.name} ({r.location}) - {r.rating}/5 - {r.cost} - {', '.join(r.cuisines[:3])}")
    
    # Test locations that should have multiple restaurants
    locations = {}
    for r in restaurants:
        locations[r.location] = locations.get(r.location, 0) + 1
    
    print(f"\n📍 Locations found: {dict(sorted(locations.items()))}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error loading data: {e}")

print("\n🏁 Test complete")
