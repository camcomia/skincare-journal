#!/usr/bin/env python3
"""
Debug tests specifically for oil-free tag issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import make_api_request, print_test_result, get_all_products, API_BASE_URL

def debug_oil_free_detection():
    """Debug oil-free tag detection logic"""
    print("🔍 Debugging Oil-Free Tag Detection")
    print("=" * 50)
    
    # Get all products
    all_products = get_all_products()
    if not all_products:
        print("❌ Could not fetch products for debugging")
        return
    
    print(f"📊 Analyzing {len(all_products)} products for oil-free detection...")
    
    # Test oil-free filter
    oil_free_response = make_api_request(API_BASE_URL, {
        "page": 1,
        "limit": 50,
        "tags": "oil-free"
    })
    
    if not oil_free_response:
        print("❌ Could not test oil-free filter")
        return
    
    oil_free_products = oil_free_response.get('products', [])
    oil_free_total = oil_free_response.get('total', 0)
    
    print(f"\n🛢️  Oil-Free Filter Results:")
    print(f"   Found {len(oil_free_products)} products (total: {oil_free_total})")
    
    # Analyze each oil-free product
    print(f"\n📋 Analyzing oil-free products:")
    for i, product in enumerate(oil_free_products[:10]):  # Analyze first 10
        name = product.get('name', '')
        ingredients = product.get('ingredientsList', '')
        brand = product.get('brand', '')
        
        print(f"\n   {i+1}. {name} ({brand})")
        print(f"      Ingredients: {ingredients[:100]}...")
        
        # Check for oil-related words
        ingredients_lower = ingredients.lower()
        name_lower = name.lower()
        
        oil_words = ['oil', 'argan', 'squalane', 'jojoba', 'coconut', 'olive', 'almond', 'sunflower', 'grapeseed', 'castor']
        found_oils = []
        
        for oil_word in oil_words:
            if oil_word in ingredients_lower or oil_word in name_lower:
                found_oils.append(oil_word)
        
        if found_oils:
            print(f"      ⚠️  WARNING: Found oil words: {found_oils}")
        else:
            print(f"      ✅ No oil words detected")
    
    # Test products that should NOT be oil-free
    print(f"\n🔍 Testing products that should NOT be oil-free:")
    
    # Look for products with obvious oil ingredients
    oil_containing_products = []
    for product in all_products:
        ingredients = product.get('ingredientsList', '').lower()
        name = product.get('name', '').lower()
        
        # Check for obvious oil ingredients
        oil_indicators = ['argan oil', 'squalane', 'jojoba oil', 'coconut oil', 'olive oil']
        for indicator in oil_indicators:
            if indicator in ingredients or indicator in name:
                oil_containing_products.append(product)
                break
    
    print(f"   Found {len(oil_containing_products)} products with obvious oil ingredients")
    
    # Test if these oil-containing products are incorrectly returned by oil-free filter
    incorrect_oil_free = []
    for product in oil_containing_products[:5]:  # Test first 5
        product_id = product.get('id')
        
        # Check if this product is in the oil-free results
        for oil_free_product in oil_free_products:
            if oil_free_product.get('id') == product_id:
                incorrect_oil_free.append(product)
                break
    
    if incorrect_oil_free:
        print(f"   ⚠️  Found {len(incorrect_oil_free)} products incorrectly tagged as oil-free:")
        for product in incorrect_oil_free:
            print(f"      - {product.get('name')} ({product.get('brand')})")
            print(f"        Ingredients: {product.get('ingredientsList', '')[:100]}...")
    else:
        print(f"   ✅ No products incorrectly tagged as oil-free")
    
    # Test backend oil detection logic
    print(f"\n🔧 Testing Backend Oil Detection Logic:")
    
    # Test specific oil detection patterns
    test_cases = [
        ("Product with Argan Oil", "Water, Argan Oil, Glycerin", True),
        ("Product with Squalane", "Water, Squalane, Niacinamide", True),
        ("Product with Jojoba Oil", "Water, Jojoba Oil, Hyaluronic Acid", True),
        ("Product with Coconut Oil", "Water, Coconut Oil, Vitamin E", True),
        ("Oil-Free Product", "Water, Glycerin, Niacinamide, Hyaluronic Acid", False),
        ("Product with 'Oil' in name", "Water, Glycerin, Niacinamide", True),  # Name contains "Oil"
    ]
    
    for test_name, test_ingredients, should_have_oil in test_cases:
        # Simulate backend logic
        ingredients_lower = test_ingredients.lower()
        name_lower = test_name.lower()
        
        oil_words = [
            "argan", "marula", "rosehip", "borage", "chia", "sea-buckthorn", 
            "squalane", "jojoba", "coconut", "olive", "almond", "sunflower",
            "grapeseed", "castor", "mineral oil", "paraffin oil", "petroleum"
        ]
        
        has_oil = False
        found_oils = []
        
        for oil_word in oil_words:
            if oil_word in ingredients_lower or oil_word in name_lower:
                has_oil = True
                found_oils.append(oil_word)
        
        # Also check for standalone "oil"
        if " oil" in ingredients_lower or ",oil" in ingredients_lower or " oil" in name_lower:
            has_oil = True
            found_oils.append("oil")
        
        result = "✅ PASS" if has_oil == should_have_oil else "❌ FAIL"
        print(f"   {result} {test_name}")
        print(f"      Expected: {'Has oil' if should_have_oil else 'No oil'}")
        print(f"      Actual: {'Has oil' if has_oil else 'No oil'}")
        if found_oils:
            print(f"      Found oils: {found_oils}")
    
    print(f"\n📊 Summary:")
    print(f"   - Total products: {len(all_products)}")
    print(f"   - Oil-free products: {len(oil_free_products)}")
    print(f"   - Products with obvious oils: {len(oil_containing_products)}")
    print(f"   - Incorrectly tagged: {len(incorrect_oil_free)}")

def test_oil_free_api_endpoint():
    """Test the oil-free API endpoint specifically"""
    print(f"\n🌐 Testing Oil-Free API Endpoint")
    print("=" * 30)
    
    # Test oil-free filter
    response = make_api_request(API_BASE_URL, {
        "page": 1,
        "limit": 20,
        "tags": "oil-free"
    })
    
    if not response:
        print_test_result("Oil-free API endpoint", False, "API request failed")
        return
    
    products = response.get('products', [])
    total = response.get('total', 0)
    
    print(f"API returned {len(products)} products (total: {total})")
    
    if products:
        print(f"\nFirst 5 oil-free products:")
        for i, product in enumerate(products[:5]):
            print(f"   {i+1}. {product.get('name')} ({product.get('brand')})")
            ingredients = product.get('ingredientsList', '')
            if ingredients:
                print(f"      Ingredients: {ingredients[:80]}...")
    
    print_test_result("Oil-free API endpoint", True, f"Found {len(products)} products")

if __name__ == "__main__":
    debug_oil_free_detection()
    test_oil_free_api_endpoint()
