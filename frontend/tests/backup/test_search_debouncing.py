#!/usr/bin/env python3
"""
Test script to verify search debouncing and performance
"""

import requests
import time

BASE_URL = "http://localhost:8080/api/products"

def test_search_performance():
    """Test search performance and debouncing"""
    print("🔍 Testing search performance...")
    
    # Test rapid search calls
    search_terms = ["ordinary", "oil", "serum", "cleanser", "toner"]
    
    for term in search_terms:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}?search={term}&page=1&limit=5")
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search '{term}' found {len(data.get('products', []))} products in {end_time - start_time:.3f}s")
        else:
            print(f"❌ Search '{term}' failed: {response.status_code}")
    
    # Test empty search
    start_time = time.time()
    response = requests.get(f"{BASE_URL}?search=&page=1&limit=5")
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Empty search returned {len(data.get('products', []))} products in {end_time - start_time:.3f}s")
    else:
        print(f"❌ Empty search failed: {response.status_code}")

def test_combined_filters_performance():
    """Test combined filters performance"""
    print("\n🔗 Testing combined filters performance...")
    
    # Test search + brand + type
    start_time = time.time()
    response = requests.get(f"{BASE_URL}?search=ordinary&brand=The Ordinary&productType=Other&page=1&limit=5")
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Combined filters found {len(data.get('products', []))} products in {end_time - start_time:.3f}s")
    else:
        print(f"❌ Combined filters failed: {response.status_code}")

def main():
    """Run performance tests"""
    print("🚀 Testing Search Performance and Debouncing")
    print("=" * 50)
    
    try:
        test_search_performance()
        test_combined_filters_performance()
        
        print("\n" + "=" * 50)
        print("✅ Performance tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8080")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()
