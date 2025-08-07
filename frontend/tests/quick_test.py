#!/usr/bin/env python3
"""
Quick test to verify API response handling
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import make_api_request, API_BASE_URL, BRANDS_API_URL

def test_api_responses():
    """Test API responses to verify they work correctly"""
    print("🧪 Testing API Responses")
    print("=" * 40)
    
    # Test basic products endpoint
    print("\n1. Testing products endpoint...")
    response = make_api_request(API_BASE_URL, {"page": 1, "limit": 5})
    if response:
        print(f"✅ Products API works")
        if isinstance(response, dict):
            print(f"   Response type: dict with {len(response.get('products', []))} products")
        elif isinstance(response, list):
            print(f"   Response type: list with {len(response)} products")
        else:
            print(f"   Response type: {type(response)}")
    else:
        print("❌ Products API failed")
    
    # Test brands endpoint
    print("\n2. Testing brands endpoint...")
    brands_response = make_api_request(BRANDS_API_URL)
    if brands_response:
        print(f"✅ Brands API works")
        if isinstance(brands_response, dict):
            print(f"   Response type: dict with {len(brands_response.get('brands', []))} brands")
        elif isinstance(brands_response, list):
            print(f"   Response type: list with {len(brands_response)} brands")
        else:
            print(f"   Response type: {type(brands_response)}")
    else:
        print("❌ Brands API failed")
    
    # Test tag filter
    print("\n3. Testing oil-free filter...")
    oil_free_response = make_api_request(API_BASE_URL, {
        "page": 1,
        "limit": 10,
        "tags": "oil-free"
    })
    if oil_free_response:
        print(f"✅ Oil-free filter works")
        if isinstance(oil_free_response, dict):
            products = oil_free_response.get('products', [])
            total = oil_free_response.get('total', 0)
        elif isinstance(oil_free_response, list):
            products = oil_free_response
            total = len(oil_free_response)
        else:
            products = []
            total = 0
        print(f"   Found {len(products)} products (total: {total})")
    else:
        print("❌ Oil-free filter failed")
    
    print("\n✅ Quick test completed!")

if __name__ == "__main__":
    test_api_responses()
