#!/usr/bin/env python3
"""
Debug script to test exact API calls
"""

import requests
import json

BASE_URL = "http://localhost:8080/api/products"

def debug_api_calls():
    """Debug API calls"""
    print("🔍 Debugging API calls...")
    
    # Test basic call
    print("\n1. Testing basic call...")
    response = requests.get(f"{BASE_URL}?page=1&limit=5")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Products returned: {len(data.get('products', []))}")
    
    # Test Oil-Free tag specifically
    print("\n2. Testing Oil-Free tag...")
    response = requests.get(f"{BASE_URL}?tags=Oil-Free&page=1&limit=10")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Products with Oil-Free: {len(data.get('products', []))}")
        for product in data.get('products', []):
            print(f"  - {product.get('name', 'N/A')}")
    
    # Test Alcohol-Free tag
    print("\n3. Testing Alcohol-Free tag...")
    response = requests.get(f"{BASE_URL}?tags=Alcohol-Free&page=1&limit=10")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Products with Alcohol-Free: {len(data.get('products', []))}")
        for product in data.get('products', []):
            print(f"  - {product.get('name', 'N/A')}")
    
    # Test debug endpoint
    print("\n4. Testing debug endpoint...")
    response = requests.get(f"{BASE_URL}/test-filters")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Debug endpoint works")

def main():
    """Run debug"""
    print("🚀 Debugging API Calls")
    print("=" * 40)
    
    try:
        debug_api_calls()
        
        print("\n" + "=" * 40)
        print("✅ API debug completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8080")
    except Exception as e:
        print(f"❌ Debug failed with error: {e}")

if __name__ == "__main__":
    main()
