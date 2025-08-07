#!/usr/bin/env python3
"""
Backend Filter Testing Script
Tests the optimized filtering functionality of the Spring Boot backend
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8080/api/products"
TEST_URL = "http://localhost:8080/api/products/test-filters"

def test_backend_connection():
    """Test if the backend is running and accessible"""
    try:
        response = requests.get(f"{BASE_URL}/all", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and accessible")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8080")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

def test_basic_pagination():
    """Test basic pagination functionality"""
    print("\n📄 Testing basic pagination...")
    
    try:
        # Test first page
        response = requests.get(f"{BASE_URL}?page=1&limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ First page: {len(data.get('products', []))} products")
            print(f"   Total: {data.get('total', 0)} products")
            print(f"   Page: {data.get('page', 0)} of {data.get('totalPages', 0)}")
        else:
            print(f"❌ Pagination test failed: {response.status_code}")
            return False
            
        # Test second page
        response = requests.get(f"{BASE_URL}?page=2&limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Second page: {len(data.get('products', []))} products")
        else:
            print(f"❌ Second page test failed: {response.status_code}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Pagination test error: {e}")
        return False

def test_product_type_filtering():
    """Test product type filtering"""
    print("\n🏷️  Testing product type filtering...")
    
    product_types = ["Cleanser", "Moisturizer", "Serum", "Sunscreen"]
    
    for product_type in product_types:
        try:
            response = requests.get(f"{BASE_URL}?productType={product_type}&page=1&limit=10")
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('products', []))
                print(f"✅ {product_type}: {count} products found")
            else:
                print(f"❌ {product_type} filter failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {product_type} filter error: {e}")

def test_tag_filtering():
    """Test tag-based filtering"""
    print("\n🏷️  Testing tag filtering...")
    
    tags = ["Alcohol-Free", "Fragrance-Free", "Oil-Free", "Sensitive Skin Friendly"]
    
    for tag in tags:
        try:
            response = requests.get(f"{BASE_URL}?tags={tag}&page=1&limit=10")
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('products', []))
                print(f"✅ {tag}: {count} products found")
            else:
                print(f"❌ {tag} filter failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {tag} filter error: {e}")

def test_combined_filtering():
    """Test combined product type and tag filtering"""
    print("\n🔗 Testing combined filtering...")
    
    test_combinations = [
        ("Cleanser", "Alcohol-Free"),
        ("Moisturizer", "Fragrance-Free"),
        ("Serum", "Oil-Free"),
        ("Sunscreen", "Sensitive Skin Friendly")
    ]
    
    for product_type, tag in test_combinations:
        try:
            response = requests.get(f"{BASE_URL}?productType={product_type}&tags={tag}&page=1&limit=10")
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('products', []))
                print(f"✅ {product_type} + {tag}: {count} products found")
            else:
                print(f"❌ {product_type} + {tag} filter failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {product_type} + {tag} filter error: {e}")

def test_filter_debug_endpoint():
    """Test the debug endpoint for filter testing"""
    print("\n🔍 Testing filter debug endpoint...")
    
    try:
        # Test with no filters
        response = requests.get(f"{TEST_URL}")
        if response.status_code == 200:
            print("✅ Debug endpoint works (no filters)")
            print(response.text[:200] + "..." if len(response.text) > 200 else response.text)
        else:
            print(f"❌ Debug endpoint failed: {response.status_code}")
            
        # Test with alcohol-free filter
        response = requests.get(f"{TEST_URL}?tags=Alcohol-Free")
        if response.status_code == 200:
            print("✅ Debug endpoint works (Alcohol-Free filter)")
        else:
            print(f"❌ Debug endpoint failed with Alcohol-Free filter: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Debug endpoint error: {e}")

def main():
    """Main test function"""
    print("🧪 Backend Filter Testing")
    print("=" * 40)
    
    # Test backend connection
    if not test_backend_connection():
        print("\n❌ Backend is not accessible. Please start the Spring Boot application.")
        sys.exit(1)
    
    # Run all tests
    test_basic_pagination()
    test_product_type_filtering()
    test_tag_filtering()
    test_combined_filtering()
    test_filter_debug_endpoint()
    
    print("\n✅ Backend filter testing completed!")
    print("\n💡 Tips:")
    print("- If filters return 0 results, check your product data")
    print("- Use the debug endpoint to see how tag matching works")
    print("- Check backend logs for detailed filtering information")

if __name__ == "__main__":
    main()
