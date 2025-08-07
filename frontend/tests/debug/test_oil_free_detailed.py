#!/usr/bin/env python3
"""
Detailed test to debug oil-free filter issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import make_api_request, API_BASE_URL

def test_specific_products():
    """Test oil-free filter with specific products"""
    print("🔍 Testing Oil-Free Filter with Specific Products")
    print("=" * 60)
    
    # First, get all products to see what we have
    print("\n1. Getting all products...")
    all_products_response = make_api_request(API_BASE_URL, {"page": 1, "limit": 50})
    
    if not all_products_response:
        print("❌ Could not get products")
        return
    
    if isinstance(all_products_response, dict):
        all_products = all_products_response.get('products', [])
    else:
        all_products = all_products_response
    
    print(f"Found {len(all_products)} total products")
    
    # Show first few products
    print("\n2. Sample products:")
    for i, product in enumerate(all_products[:5]):
        name = product.get('name', '')
        ingredients = product.get('ingredientsList', '')
        brand = product.get('brand', '')
        print(f"   {i+1}. {name} ({brand})")
        print(f"      Ingredients: {ingredients[:100]}...")
    
    # Test oil-free filter
    print("\n3. Testing oil-free filter...")
    oil_free_response = make_api_request(API_BASE_URL, {
        "page": 1,
        "limit": 50,
        "tags": "oil-free"
    })
    
    if not oil_free_response:
        print("❌ Oil-free filter request failed")
        return
    
    if isinstance(oil_free_response, dict):
        oil_free_products = oil_free_response.get('products', [])
        total = oil_free_response.get('total', 0)
    else:
        oil_free_products = oil_free_response
        total = len(oil_free_response)
    
    print(f"Oil-free filter returned {len(oil_free_products)} products (total: {total})")
    
    if oil_free_products:
        print("\nOil-free products found:")
        for i, product in enumerate(oil_free_products):
            name = product.get('name', '')
            ingredients = product.get('ingredientsList', '')
            brand = product.get('brand', '')
            print(f"   {i+1}. {name} ({brand})")
            print(f"      Ingredients: {ingredients[:100]}...")
    else:
        print("No oil-free products found")
    
    # Test individual tag filters
    print("\n4. Testing individual tag filters...")
    tags_to_test = ['alcohol-free', 'fragrance-free', 'sensitive skin friendly']
    
    for tag in tags_to_test:
        response = make_api_request(API_BASE_URL, {
            "page": 1,
            "limit": 20,
            "tags": tag
        })
        
        if response:
            if isinstance(response, dict):
                products = response.get('products', [])
                total = response.get('total', 0)
            else:
                products = response
                total = len(response)
            
            print(f"   {tag}: {len(products)} products (total: {total})")
        else:
            print(f"   {tag}: Failed")
    
    # Test products that should NOT be oil-free
    print("\n5. Testing products that should NOT be oil-free...")
    
    # Look for products with obvious oil ingredients
    oil_containing_products = []
    for product in all_products:
        ingredients = product.get('ingredientsList', '').lower()
        name = product.get('name', '').lower()
        
        # Check for obvious oil ingredients
        oil_indicators = ['argan oil', 'squalane', 'jojoba oil', 'coconut oil', 'olive oil', 'oil']
        for indicator in oil_indicators:
            if indicator in ingredients or indicator in name:
                oil_containing_products.append(product)
                break
    
    print(f"Found {len(oil_containing_products)} products with obvious oil ingredients:")
    for product in oil_containing_products:
        name = product.get('name', '')
        ingredients = product.get('ingredientsList', '')
        brand = product.get('brand', '')
        print(f"   - {name} ({brand})")
        print(f"     Ingredients: {ingredients[:100]}...")
    
    # Test if these oil-containing products are incorrectly returned by oil-free filter
    incorrect_oil_free = []
    for product in oil_containing_products:
        product_id = product.get('id')
        
        # Check if this product is in the oil-free results
        for oil_free_product in oil_free_products:
            if oil_free_product.get('id') == product_id:
                incorrect_oil_free.append(product)
                break
    
    if incorrect_oil_free:
        print(f"\n⚠️  Found {len(incorrect_oil_free)} products incorrectly tagged as oil-free:")
        for product in incorrect_oil_free:
            print(f"   - {product.get('name')} ({product.get('brand')})")
    else:
        print(f"\n✅ No products incorrectly tagged as oil-free")

if __name__ == "__main__":
    test_specific_products()
