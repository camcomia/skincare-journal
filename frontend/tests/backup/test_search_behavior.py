#!/usr/bin/env python3
"""
Test script for new search behavior (triggered on blur/enter)
"""

import requests
import time

BASE_URL = "http://localhost:8080/api/products"

def test_search_behavior():
    """Test the new search behavior"""
    print("🔍 Testing new search behavior...")
    
    # Test that search works correctly
    search_terms = ["ordinary", "oil", "serum", "cleanser", "toner"]
    
    for term in search_terms:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}?search={term}&page=1&limit=5")
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"✅ Search '{term}' found {len(products)} products in {end_time - start_time:.3f}s")
            
            # Verify search results are relevant
            for product in products:
                name = product.get('name', '').lower()
                brand = product.get('brand', '').lower()
                ingredients = product.get('ingredientsList', '').lower()
                
                if term.lower() not in name and term.lower() not in brand and term.lower() not in ingredients:
                    print(f"  ⚠️  Unexpected result for '{term}': {product.get('name')}")
        else:
            print(f"❌ Search '{term}' failed: {response.status_code}")
    
    # Test empty search
    start_time = time.time()
    response = requests.get(f"{BASE_URL}?search=&page=1&limit=5")
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ Empty search returned {len(products)} products in {end_time - start_time:.3f}s")
    else:
        print(f"❌ Empty search failed: {response.status_code}")

def test_search_performance():
    """Test search performance"""
    print("\n⚡ Testing search performance...")
    
    # Test multiple rapid searches
    search_terms = ["ordinary", "garnier", "cosrx", "numbuzin"]
    
    total_time = 0
    total_searches = 0
    
    for term in search_terms:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}?search={term}&page=1&limit=5")
        end_time = time.time()
        
        if response.status_code == 200:
            total_time += (end_time - start_time)
            total_searches += 1
            print(f"✅ Search '{term}' completed in {end_time - start_time:.3f}s")
        else:
            print(f"❌ Search '{term}' failed: {response.status_code}")
    
    if total_searches > 0:
        avg_time = total_time / total_searches
        print(f"\n📊 Performance Summary:")
        print(f"   Total searches: {total_searches}")
        print(f"   Average response time: {avg_time:.3f}s")
        print(f"   Total time: {total_time:.3f}s")

def test_search_accuracy():
    """Test search accuracy"""
    print("\n🎯 Testing search accuracy...")
    
    # Test specific search scenarios
    test_cases = [
        ("ordinary", "Should find The Ordinary products"),
        ("garnier", "Should find Garnier products"),
        ("oil", "Should find products with oil in name/ingredients"),
        ("serum", "Should find serum products"),
        ("xyz123", "Should return no results for non-existent term")
    ]
    
    for search_term, description in test_cases:
        response = requests.get(f"{BASE_URL}?search={search_term}&page=1&limit=10")
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            
            if search_term == "xyz123":
                if len(products) == 0:
                    print(f"✅ {description}: No results (correct)")
                else:
                    print(f"❌ {description}: Found {len(products)} unexpected results")
            else:
                print(f"✅ {description}: Found {len(products)} results")
                
                # Show first few results
                for i, product in enumerate(products[:3]):
                    print(f"   {i+1}. {product.get('name', 'N/A')} ({product.get('brand', 'N/A')})")
        else:
            print(f"❌ Search '{search_term}' failed: {response.status_code}")

def main():
    """Run search behavior tests"""
    print("🚀 Testing New Search Behavior")
    print("=" * 50)
    
    try:
        test_search_behavior()
        test_search_performance()
        test_search_accuracy()
        
        print("\n" + "=" * 50)
        print("✅ Search behavior tests completed!")
        print("\n📝 Note: Frontend search now triggers on:")
        print("   - User pressing Enter")
        print("   - User leaving the search field (blur)")
        print("   - User clearing the search")
        print("   (No more debounce delay)")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8080")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()
