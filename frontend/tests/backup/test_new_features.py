#!/usr/bin/env python3
"""
Test script for new features: search, brand filtering, and sorting
"""

import requests
import json
import time

BASE_URL = "http://localhost:8080/api/products"

def test_search_functionality():
    """Test search functionality"""
    print("🔍 Testing search functionality...")
    
    # Test search by product name
    response = requests.get(f"{BASE_URL}?search=ordinary&page=1&limit=5")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Search 'ordinary' found {len(data.get('products', []))} products")
    else:
        print(f"❌ Search failed: {response.status_code}")
    
    # Test search by brand
    response = requests.get(f"{BASE_URL}?search=garnier&page=1&limit=5")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Search 'garnier' found {len(data.get('products', []))} products")
    else:
        print(f"❌ Search failed: {response.status_code}")

def test_brand_filtering():
    """Test brand filtering"""
    print("\n🏷️ Testing brand filtering...")
    
    # Test brand filter
    response = requests.get(f"{BASE_URL}?brand=The Ordinary&page=1&limit=5")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Brand filter 'The Ordinary' found {len(data.get('products', []))} products")
    else:
        print(f"❌ Brand filter failed: {response.status_code}")

def test_sorting():
    """Test sorting functionality"""
    print("\n📊 Testing sorting functionality...")
    
    # Test name sorting
    response = requests.get(f"{BASE_URL}?sortBy=name&page=1&limit=5")
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        if products:
            print(f"✅ Name sorting works - First product: {products[0].get('name', 'N/A')}")
    else:
        print(f"❌ Name sorting failed: {response.status_code}")
    
    # Test price sorting
    response = requests.get(f"{BASE_URL}?sortBy=price&page=1&limit=5")
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        if products:
            print(f"✅ Price sorting works - First product price: {products[0].get('price', 'N/A')}")
    else:
        print(f"❌ Price sorting failed: {response.status_code}")

def test_brands_endpoint():
    """Test the brands endpoint"""
    print("\n🏪 Testing brands endpoint...")
    
    response = requests.get(f"{BASE_URL}/brands")
    if response.status_code == 200:
        brands = response.json()
        print(f"✅ Brands endpoint works - Found {len(brands)} brands: {', '.join(brands[:5])}")
    else:
        print(f"❌ Brands endpoint failed: {response.status_code}")

def test_combined_filters():
    """Test combined filters"""
    print("\n🔗 Testing combined filters...")
    
    # Test search + brand + type
    response = requests.get(f"{BASE_URL}?search=oil&brand=The Ordinary&productType=Other&page=1&limit=5")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Combined filters work - Found {len(data.get('products', []))} products")
    else:
        print(f"❌ Combined filters failed: {response.status_code}")

def test_performance():
    """Test performance with large datasets"""
    print("\n⚡ Testing performance...")
    
    start_time = time.time()
    response = requests.get(f"{BASE_URL}?page=1&limit=10")
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Performance test - {len(data.get('products', []))} products in {end_time - start_time:.3f}s")
    else:
        print(f"❌ Performance test failed: {response.status_code}")

def main():
    """Run all tests"""
    print("🚀 Testing new features: Search, Brand Filtering, and Sorting")
    print("=" * 60)
    
    try:
        test_search_functionality()
        test_brand_filtering()
        test_sorting()
        test_brands_endpoint()
        test_combined_filters()
        test_performance()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8080")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()
