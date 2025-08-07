#!/usr/bin/env python3
"""
Test script specifically for tag filtering functionality
"""

import requests
import json

BASE_URL = "http://localhost:8080/api/products"

def test_tag_filtering():
    """Test tag filtering functionality"""
    print("🏷️ Testing tag filtering functionality...")
    
    # Test Alcohol-Free tag
    response = requests.get(f"{BASE_URL}?tags=Alcohol-Free&page=1&limit=10")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Alcohol-Free filter found {len(data.get('products', []))} products")
    else:
        print(f"❌ Alcohol-Free filter failed: {response.status_code}")
    
    # Test Oil-Free tag
    response = requests.get(f"{BASE_URL}?tags=Oil-Free&page=1&limit=10")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Oil-Free filter found {len(data.get('products', []))} products")
    else:
        print(f"❌ Oil-Free filter failed: {response.status_code}")
    
    # Test Fragrance-Free tag
    response = requests.get(f"{BASE_URL}?tags=Fragrance-Free&page=1&limit=10")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Fragrance-Free filter found {len(data.get('products', []))} products")
    else:
        print(f"❌ Fragrance-Free filter failed: {response.status_code}")
    
    # Test Sensitive Skin Friendly tag
    response = requests.get(f"{BASE_URL}?tags=Sensitive Skin Friendly&page=1&limit=10")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sensitive Skin Friendly filter found {len(data.get('products', []))} products")
    else:
        print(f"❌ Sensitive Skin Friendly filter failed: {response.status_code}")
    
    # Test multiple tags
    response = requests.get(f"{BASE_URL}?tags=Alcohol-Free,Oil-Free&page=1&limit=10")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Multiple tags filter found {len(data.get('products', []))} products")
    else:
        print(f"❌ Multiple tags filter failed: {response.status_code}")

def test_combined_filters_with_tags():
    """Test combined filters with tags"""
    print("\n🔗 Testing combined filters with tags...")
    
    # Test search + tag
    response = requests.get(f"{BASE_URL}?search=ordinary&tags=Alcohol-Free&page=1&limit=10")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Search + tag filter found {len(data.get('products', []))} products")
    else:
        print(f"❌ Search + tag filter failed: {response.status_code}")
    
    # Test brand + tag
    response = requests.get(f"{BASE_URL}?brand=The Ordinary&tags=Oil-Free&page=1&limit=10")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Brand + tag filter found {len(data.get('products', []))} products")
    else:
        print(f"❌ Brand + tag filter failed: {response.status_code}")

def main():
    """Run tag filtering tests"""
    print("🚀 Testing Tag Filtering Functionality")
    print("=" * 50)
    
    try:
        test_tag_filtering()
        test_combined_filters_with_tags()
        
        print("\n" + "=" * 50)
        print("✅ Tag filtering tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8080")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()
