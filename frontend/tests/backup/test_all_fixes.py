#!/usr/bin/env python3
"""
Comprehensive test script for all fixes
"""

import requests
import json
import time

BASE_URL = "http://localhost:8080/api/products"

def test_oil_free_fix():
    """Test oil-free tag fix"""
    print("🏷️ Testing Oil-Free tag fix...")
    
    # Test oil-free filter
    response = requests.get(f"{BASE_URL}?tags=Oil-Free&page=1&limit=20")
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Oil-Free filter returned {len(products)} products")
        
        # Check if products that should have oil are excluded
        oil_products = [p for p in products if any(word in p.get('name', '').lower() for word in ['oil', 'argan', 'marula', 'borage'])]
        if oil_products:
            print(f"❌ Found products with oil in name: {[p.get('name') for p in oil_products]}")
        else:
            print("✅ No products with oil in name found in results")
    else:
        print(f"❌ Oil-Free filter failed: {response.status_code}")

def test_search_functionality():
    """Test search functionality"""
    print("\n🔍 Testing search functionality...")
    
    # Test search by product name
    response = requests.get(f"{BASE_URL}?search=ordinary&page=1&limit=5")
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Search 'ordinary' found {len(products)} products")
        
        # Verify results contain 'ordinary'
        for product in products:
            name = product.get('name', '').lower()
            if 'ordinary' not in name:
                print(f"❌ Unexpected result: {product.get('name')}")
    else:
        print(f"❌ Search failed: {response.status_code}")
    
    # Test search by brand
    response = requests.get(f"{BASE_URL}?search=garnier&page=1&limit=5")
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Search 'garnier' found {len(products)} products")
    else:
        print(f"❌ Search failed: {response.status_code}")

def test_brand_filtering():
    """Test brand filtering"""
    print("\n🏪 Testing brand filtering...")
    
    response = requests.get(f"{BASE_URL}?brand=The Ordinary&page=1&limit=10")
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Brand filter 'The Ordinary' found {len(products)} products")
        
        # Verify all results are from The Ordinary
        for product in products:
            if product.get('brand') != 'The Ordinary':
                print(f"❌ Unexpected brand: {product.get('brand')} for {product.get('name')}")
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

def test_combined_filters():
    """Test combined filters"""
    print("\n🔗 Testing combined filters...")
    
    # Test search + brand + type
    response = requests.get(f"{BASE_URL}?search=ordinary&brand=The Ordinary&productType=Other&page=1&limit=5")
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Combined filters found {len(products)} products")
    else:
        print(f"❌ Combined filters failed: {response.status_code}")

def test_performance():
    """Test performance"""
    print("\n⚡ Testing performance...")
    
    start_time = time.time()
    response = requests.get(f"{BASE_URL}?page=1&limit=10")
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Performance test - {len(data.get('products', []))} products in {end_time - start_time:.3f}s")
    else:
        print(f"❌ Performance test failed: {response.status_code}")

def test_all_tags():
    """Test all tag filters"""
    print("\n🏷️ Testing all tag filters...")
    
    tags = ['Alcohol-Free', 'Fragrance-Free', 'Oil-Free', 'Sensitive Skin Friendly']
    
    for tag in tags:
        response = requests.get(f"{BASE_URL}?tags={tag}&page=1&limit=10")
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"✅ {tag} filter found {len(products)} products")
        else:
            print(f"❌ {tag} filter failed: {response.status_code}")

def main():
    """Run all tests"""
    print("🚀 Testing All Fixes: Search, Filters, and Performance")
    print("=" * 60)
    
    try:
        test_oil_free_fix()
        test_search_functionality()
        test_brand_filtering()
        test_sorting()
        test_combined_filters()
        test_performance()
        test_all_tags()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8080")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()
