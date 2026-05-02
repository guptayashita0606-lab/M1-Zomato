#!/usr/bin/env python3
"""
Debug script to test Hugging Face data loading step by step.
"""

import sys
import os
sys.path.append('src')

print("=== Hugging Face Data Loading Debug ===")

# Test 1: Check datasets package
try:
    print("1. Testing datasets package import...")
    from datasets import load_dataset
    print("✅ datasets package imported successfully")
except ImportError as e:
    print(f"❌ datasets package import failed: {e}")
    exit(1)

# Test 2: Try loading dataset with minimal configuration
try:
    print("\n2. Testing dataset loading...")
    print(f"   Dataset name: ManikaSaini/zomato-restaurant-recommendation")
    print(f"   Split: train")
    print(f"   Revision: main")
    
    dataset = load_dataset(
        "ManikaSaini/zomato-restaurant-recommendation",
        split="train",
        revision="main",
        streaming=True  # Try streaming to avoid memory issues
    )
    print("✅ Dataset loaded successfully")
    
    # Test 3: Try to get first few rows
    print("\n3. Testing data access...")
    count = 0
    for row in dataset:
        print(f"   Row {count + 1}: {row}")
        count += 1
        if count >= 3:  # Just test first 3 rows
            break
    
    print(f"✅ Successfully accessed {count} rows")
    
except Exception as e:
    print(f"❌ Dataset loading failed: {e}")
    print(f"   Error type: {type(e).__name__}")
    
    # Try alternative approach
    print("\n4. Trying alternative approach...")
    try:
        dataset = load_dataset(
            "ManikaSaini/zomato-restaurant-recommendation",
            split="train",
            revision="main"
        )
        print("✅ Dataset loaded with alternative approach")
        
        # Test with limited rows
        print("\n5. Testing limited data access...")
        limited_data = dataset.select(range(5))  # Get first 5 rows
        for i, row in enumerate(limited_data):
            print(f"   Row {i + 1}: {row}")
        
        print(f"✅ Successfully accessed {len(limited_data)} rows")
        
    except Exception as e2:
        print(f"❌ Alternative approach also failed: {e2}")
        print(f"   Error type: {type(e2).__name__}")

print("\n=== Debug Complete ===")
