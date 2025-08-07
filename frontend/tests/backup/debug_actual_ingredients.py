#!/usr/bin/env python3
"""
Debug script to see actual ingredient names
"""

import requests
import json

BASE_URL = "http://localhost:8080/api/products"

def debug_actual_ingredients():
    """Debug actual ingredient names"""
    print("🔍 Debugging actual ingredient names...")
    
    # Get all products
    response = requests.get(f"{BASE_URL}?page=1&limit=20")
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        
        print(f"Found {len(products)} products")
        print("\nActual ingredient names:")
        
        for i, product in enumerate(products[:5]):
            name = product.get('name', 'N/A')
            ingredients = product.get('ingredientsList', 'N/A')
            
            print(f"\n{i+1}. {name}")
            print(f"   Full ingredients: {ingredients}")
            
            # Check for any oil-related words
            ingredients_lower = ingredients.lower()
            oil_indicators = ['oil', 'argan', 'marula', 'rosehip', 'borage', 'chia', 'sea-buckthorn', 'squalane']
            
            found_oils = []
            for indicator in oil_indicators:
                if indicator in ingredients_lower:
                    found_oils.append(indicator)
            
            if found_oils:
                print(f"   Found oil indicators: {', '.join(found_oils)}")
            else:
                print(f"   No oil indicators found")

def main():
    """Run ingredient debug"""
    print("🚀 Debugging Actual Ingredient Names")
    print("=" * 50)
    
    try:
        debug_actual_ingredients()
        
        print("\n" + "=" * 50)
        print("✅ Ingredient debug completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8080")
    except Exception as e:
        print(f"❌ Debug failed with error: {e}")

if __name__ == "__main__":
    main()
