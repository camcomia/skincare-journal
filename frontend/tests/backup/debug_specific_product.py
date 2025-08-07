#!/usr/bin/env python3
"""
Debug script for specific product that's incorrectly showing up in oil-free results
"""

import requests
import json

BASE_URL = "http://localhost:8080/api/products"

def debug_specific_product():
    """Debug the specific product issue"""
    print("🔍 Debugging specific product issue...")
    
    # Get the specific product
    response = requests.get(f"{BASE_URL}?search=chia seed oil&page=1&limit=5")
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        
        for product in products:
            name = product.get('name', 'N/A')
            ingredients = product.get('ingredientsList', 'N/A')
            
            print(f"\nProduct: {name}")
            print(f"Ingredients: {ingredients}")
            
            # Check oil detection
            ingredients_lower = ingredients.lower()
            oil_words = ['argan', 'marula', 'rosehip', 'borage', 'chia', 'sea-buckthorn', 'squalane', 'jojoba', 'coconut', 'olive', 'almond', 'sunflower', 'grapeseed', 'castor']
            
            found_oils = []
            for oil_word in oil_words:
                if oil_word in ingredients_lower:
                    found_oils.append(oil_word)
            
            if found_oils:
                print(f"Found oils: {', '.join(found_oils)}")
                print(f"Should be Oil-Free: False")
            else:
                print(f"No oils found")
                print(f"Should be Oil-Free: True")
    
    # Test oil-free filter specifically
    print(f"\n🔗 Testing Oil-Free filter...")
    response = requests.get(f"{BASE_URL}?tags=Oil-Free&page=1&limit=20")
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        
        print(f"Oil-Free filter returned {len(products)} products:")
        for product in products:
            name = product.get('name', 'N/A')
            ingredients = product.get('ingredientsList', 'N/A')
            
            # Check if this product should actually be oil-free
            ingredients_lower = ingredients.lower()
            oil_words = ['argan', 'marula', 'rosehip', 'borage', 'chia', 'sea-buckthorn', 'squalane', 'jojoba', 'coconut', 'olive', 'almond', 'sunflower', 'grapeseed', 'castor']
            
            found_oils = []
            for oil_word in oil_words:
                if oil_word in ingredients_lower:
                    found_oils.append(oil_word)
            
            if found_oils:
                print(f"❌ {name} - HAS OILS: {', '.join(found_oils)}")
            else:
                print(f"✅ {name} - OIL FREE")

def main():
    """Run debug"""
    print("🚀 Debugging Specific Product Issue")
    print("=" * 50)
    
    try:
        debug_specific_product()
        
        print("\n" + "=" * 50)
        print("✅ Debug completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8080")
    except Exception as e:
        print(f"❌ Debug failed with error: {e}")

if __name__ == "__main__":
    main()
