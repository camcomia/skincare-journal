#!/usr/bin/env python3
"""
Test to verify backend logic is working correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import make_api_request, API_BASE_URL

def test_backend_logic():
    """Test backend logic with specific products"""
    print("🔍 Testing Backend Logic")
    print("=" * 40)
    
    # Test products that should be sensitive skin friendly
    print("\n1. Testing products that should be sensitive skin friendly...")
    
    # Test with a product that has no irritants and no oils
    test_response = make_api_request(API_BASE_URL, {
        "page": 1,
        "limit": 20,
        "tags": "sensitive skin friendly"
    })
    
    if test_response:
        if isinstance(test_response, dict):
            products = test_response.get('products', [])
            total = test_response.get('total', 0)
        else:
            products = test_response
            total = len(test_response)
        
        print(f"Sensitive skin friendly filter returned {len(products)} products (total: {total})")
        
        if products:
            print("\nProducts found:")
            for i, product in enumerate(products[:5]):  # Show first 5
                name = product.get('name', '')
                ingredients = product.get('ingredientsList', '')
                brand = product.get('brand', '')
                print(f"   {i+1}. {name} ({brand})")
                print(f"      Ingredients: {ingredients[:80]}...")
                
                # Check if this product actually should be sensitive skin friendly
                ingredients_lower = ingredients.lower()
                name_lower = name.lower()
                
                # Check for irritants
                irritants = ['alcohol', 'fragrance', 'menthol', 'peppermint', 'eucalyptus', 'camphor', 'sodium lauryl sulfate', 'sls', 'sodium laureth sulfate', 'sles', 'witch hazel']
                found_irritants = []
                for irritant in irritants:
                    if irritant in ingredients_lower or irritant in name_lower:
                        found_irritants.append(irritant)
                
                # Check for oils
                oils = ['oil', 'argan', 'squalane', 'jojoba', 'coconut', 'olive', 'almond', 'sunflower', 'grapeseed', 'castor']
                found_oils = []
                for oil in oils:
                    if oil in ingredients_lower or oil in name_lower:
                        found_oils.append(oil)
                
                should_be_sensitive = len(found_irritants) == 0 and len(found_oils) == 0
                status = "✅ CORRECT" if should_be_sensitive else "❌ INCORRECT"
                print(f"      {status} - Irritants: {found_irritants}, Oils: {found_oils}")
        else:
            print("No products found")
    else:
        print("❌ Filter request failed")
    
    # Test individual filters
    print("\n2. Testing individual filters...")
    filters_to_test = [
        ("alcohol-free", "Products without alcohol"),
        ("fragrance-free", "Products without fragrance"),
        ("oil-free", "Products without oils"),
        ("sensitive skin friendly", "Products without irritants and oils")
    ]
    
    for filter_tag, description in filters_to_test:
        response = make_api_request(API_BASE_URL, {
            "page": 1,
            "limit": 10,
            "tags": filter_tag
        })
        
        if response:
            if isinstance(response, dict):
                products = response.get('products', [])
                total = response.get('total', 0)
            else:
                products = response
                total = len(response)
            
            print(f"   {filter_tag}: {len(products)} products (total: {total})")
            
            if products:
                # Show first product as example
                first_product = products[0]
                name = first_product.get('name', '')
                ingredients = first_product.get('ingredientsList', '')
                print(f"      Example: {name}")
                print(f"      Ingredients: {ingredients[:60]}...")
        else:
            print(f"   {filter_tag}: Failed")

if __name__ == "__main__":
    test_backend_logic()
