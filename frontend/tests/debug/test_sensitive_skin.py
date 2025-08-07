#!/usr/bin/env python3
"""
Test to debug sensitive skin friendly filter
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import make_api_request, API_BASE_URL

def test_sensitive_skin_filter():
    """Test sensitive skin friendly filter specifically"""
    print("🔍 Testing Sensitive Skin Friendly Filter")
    print("=" * 50)
    
    # Get all products first
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
    
    # Test sensitive skin friendly filter
    print("\n2. Testing sensitive skin friendly filter...")
    sensitive_response = make_api_request(API_BASE_URL, {
        "page": 1,
        "limit": 50,
        "tags": "sensitive skin friendly"
    })
    
    if not sensitive_response:
        print("❌ Sensitive skin filter request failed")
        return
    
    if isinstance(sensitive_response, dict):
        sensitive_products = sensitive_response.get('products', [])
        total = sensitive_response.get('total', 0)
    else:
        sensitive_products = sensitive_response
        total = len(sensitive_response)
    
    print(f"Sensitive skin friendly filter returned {len(sensitive_products)} products (total: {total})")
    
    if sensitive_products:
        print("\nSensitive skin friendly products found:")
        for i, product in enumerate(sensitive_products):
            name = product.get('name', '')
            ingredients = product.get('ingredientsList', '')
            brand = product.get('brand', '')
            print(f"   {i+1}. {name} ({brand})")
            print(f"      Ingredients: {ingredients[:100]}...")
    else:
        print("No sensitive skin friendly products found")
    
    # Analyze products that should NOT be sensitive skin friendly
    print("\n3. Analyzing products that should NOT be sensitive skin friendly...")
    
    # Check for products with irritants
    irritant_products = []
    for product in all_products:
        ingredients = product.get('ingredientsList', '').lower()
        name = product.get('name', '').lower()
        
        # Check for irritants
        irritants = ['alcohol', 'fragrance', 'menthol', 'peppermint', 'eucalyptus', 'camphor', 'sodium lauryl sulfate', 'sls', 'sodium laureth sulfate', 'sles', 'witch hazel']
        found_irritants = []
        
        for irritant in irritants:
            if irritant in ingredients or irritant in name:
                found_irritants.append(irritant)
        
        if found_irritants:
            irritant_products.append({
                'product': product,
                'irritants': found_irritants
            })
    
    print(f"Found {len(irritant_products)} products with irritants:")
    for item in irritant_products:
        product = item['product']
        irritants = item['irritants']
        name = product.get('name', '')
        brand = product.get('brand', '')
        ingredients = product.get('ingredientsList', '')
        print(f"   - {name} ({brand})")
        print(f"     Irritants: {irritants}")
        print(f"     Ingredients: {ingredients[:100]}...")
    
    # Check if irritant products are incorrectly included in sensitive skin results
    incorrect_sensitive = []
    for item in irritant_products:
        product = item['product']
        product_id = product.get('id')
        
        # Check if this product is in the sensitive skin results
        for sensitive_product in sensitive_products:
            if sensitive_product.get('id') == product_id:
                incorrect_sensitive.append(item)
                break
    
    if incorrect_sensitive:
        print(f"\n⚠️  Found {len(incorrect_sensitive)} products incorrectly tagged as sensitive skin friendly:")
        for item in incorrect_sensitive:
            product = item['product']
            irritants = item['irritants']
            print(f"   - {product.get('name')} ({product.get('brand')})")
            print(f"     Irritants: {irritants}")
    else:
        print(f"\n✅ No products incorrectly tagged as sensitive skin friendly")
    
    # Test individual irritant detection
    print("\n4. Testing individual irritant detection...")
    test_cases = [
        ("Product with Alcohol", "Water, Alcohol Denat., Glycerin", ["alcohol"]),
        ("Product with Fragrance", "Water, Fragrance, Niacinamide", ["fragrance"]),
        ("Product with Menthol", "Water, Menthol, Hyaluronic Acid", ["menthol"]),
        ("Product with SLS", "Water, Sodium Lauryl Sulfate, Glycerin", ["sodium lauryl sulfate"]),
        ("Sensitive Skin Product", "Water, Glycerin, Niacinamide, Hyaluronic Acid", []),
    ]
    
    for test_name, test_ingredients, expected_irritants in test_cases:
        ingredients_lower = test_ingredients.lower()
        irritants = ['alcohol', 'fragrance', 'menthol', 'peppermint', 'eucalyptus', 'camphor', 'sodium lauryl sulfate', 'sls', 'sodium laureth sulfate', 'sles', 'witch hazel']
        found_irritants = []
        
        for irritant in irritants:
            if irritant in ingredients_lower:
                found_irritants.append(irritant)
        
        is_sensitive_friendly = len(found_irritants) == 0
        result = "✅ PASS" if found_irritants == expected_irritants else "❌ FAIL"
        print(f"   {result} {test_name}")
        print(f"      Expected irritants: {expected_irritants}")
        print(f"      Found irritants: {found_irritants}")
        print(f"      Sensitive skin friendly: {is_sensitive_friendly}")

if __name__ == "__main__":
    test_sensitive_skin_filter()
