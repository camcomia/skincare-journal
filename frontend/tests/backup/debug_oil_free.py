#!/usr/bin/env python3
"""
Debug script specifically for oil-free tag issue
"""

import requests
import json

BASE_URL = "http://localhost:8080/api/products"

def debug_oil_free():
    """Debug oil-free tag specifically"""
    print("🔍 Debugging Oil-Free tag issue...")
    
    # Get all products
    response = requests.get(f"{BASE_URL}?page=1&limit=20")
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        
        print(f"Found {len(products)} products")
        print("\nChecking Oil-Free detection:")
        
        oil_free_products = []
        non_oil_free_products = []
        
        for product in products:
            name = product.get('name', 'N/A')
            ingredients = product.get('ingredientsList', '').lower()
            
            # Check for oils using the same logic as backend
            oils = [
                "olive oil", "coconut oil", "jojoba oil", "argan oil", "rosehip oil",
                "marula oil", "chia seed oil", "sea-buckthorn oil", "borage seed oil",
                "moroccan argan oil", "virgin argan oil", "cold-pressed virgin marula oil",
                "organic cold-pressed borage seed oil", "organic virgin chia seed oil",
                "organic virgin sea-buckthorn fruit oil", "plant-derived hemi-squalane"
            ]
            
            has_oil = any(oil in ingredients for oil in oils)
            
            if has_oil:
                non_oil_free_products.append(name)
                print(f"❌ {name} - HAS OIL")
                print(f"   Ingredients: {ingredients[:100]}...")
            else:
                oil_free_products.append(name)
                print(f"✅ {name} - OIL FREE")
        
        print(f"\n📊 Summary:")
        print(f"Oil-Free products: {len(oil_free_products)}")
        print(f"Non-Oil-Free products: {len(non_oil_free_products)}")
        
        # Test the API call
        print(f"\n🔗 Testing API call for Oil-Free...")
        response = requests.get(f"{BASE_URL}?tags=Oil-Free&page=1&limit=20")
        if response.status_code == 200:
            data = response.json()
            api_products = data.get('products', [])
            print(f"API returned {len(api_products)} Oil-Free products")
            
            for product in api_products:
                print(f"  - {product.get('name', 'N/A')}")
        else:
            print(f"❌ API call failed: {response.status_code}")

def test_oil_detection():
    """Test specific oil detection patterns"""
    print("\n🧪 Testing oil detection patterns...")
    
    test_ingredients = [
        "Aqua, Glycerin, Argan Oil, Rosehip Oil",
        "Water, Glycerin, Hyaluronic Acid",
        "Aqua, Marula Oil, Coconut Oil, Jojoba Oil",
        "Water, Niacinamide, Panthenol",
        "Aqua, Borage Seed Oil, Chia Seed Oil"
    ]
    
    oils = [
        "olive oil", "coconut oil", "jojoba oil", "argan oil", "rosehip oil",
        "marula oil", "chia seed oil", "sea-buckthorn oil", "borage seed oil",
        "moroccan argan oil", "virgin argan oil", "cold-pressed virgin marula oil",
        "organic cold-pressed borage seed oil", "organic virgin chia seed oil",
        "organic virgin sea-buckthorn fruit oil", "plant-derived hemi-squalane"
    ]
    
    for i, ingredients in enumerate(test_ingredients, 1):
        ingredients_lower = ingredients.lower()
        has_oil = any(oil in ingredients_lower for oil in oils)
        print(f"{i}. {ingredients}")
        print(f"   Has oil: {has_oil}")
        print(f"   Oil-Free: {not has_oil}")
        print()

def main():
    """Run oil-free debug"""
    print("🚀 Debugging Oil-Free Tag Issue")
    print("=" * 50)
    
    try:
        debug_oil_free()
        test_oil_detection()
        
        print("\n" + "=" * 50)
        print("✅ Oil-Free debug completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8080")
    except Exception as e:
        print(f"❌ Debug failed with error: {e}")

if __name__ == "__main__":
    main()
