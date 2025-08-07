#!/usr/bin/env python3
"""
Debug script to check ingredients and tag detection
"""

import requests
import json

BASE_URL = "http://localhost:8080/api/products"

def debug_ingredients():
    """Debug ingredients and tag detection"""
    print("🔍 Debugging ingredients and tag detection...")
    
    # Get all products
    response = requests.get(f"{BASE_URL}?page=1&limit=20")
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        
        print(f"Found {len(products)} products")
        print("\nSample products with ingredients:")
        
        for i, product in enumerate(products[:5]):
            print(f"\n{i+1}. {product.get('name', 'N/A')}")
            print(f"   Brand: {product.get('brand', 'N/A')}")
            print(f"   Ingredients: {product.get('ingredientsList', 'N/A')[:200]}...")
            
            # Check tag detection
            ingredients = product.get('ingredientsList', '').lower()
            
            # Check for bad alcohols
            bad_alcohols = ['alcohol', 'alcohol denat', 'ethanol', 'ethyl alcohol', 'isopropyl alcohol']
            has_bad_alcohol = any(alcohol in ingredients for alcohol in bad_alcohols)
            print(f"   Has bad alcohol: {has_bad_alcohol}")
            
            # Check for fragrances
            fragrances = ['fragrance', 'parfum', 'perfume', 'aroma']
            has_fragrance = any(frag in ingredients for frag in fragrances)
            print(f"   Has fragrance: {has_fragrance}")
            
            # Check for oils
            oils = ['oil', 'olive oil', 'coconut oil', 'jojoba oil', 'argan oil']
            has_oil = any(oil in ingredients for oil in oils)
            print(f"   Has oil: {has_oil}")
            
            # Check for irritants
            irritants = ['menthol', 'peppermint', 'eucalyptus', 'camphor', 'sodium lauryl sulfate']
            has_irritant = any(irritant in ingredients for irritant in irritants)
            print(f"   Has irritant: {has_irritant}")
            
            # Determine tags
            tags = []
            if not has_bad_alcohol:
                tags.append('Alcohol-Free')
            if not has_fragrance:
                tags.append('Fragrance-Free')
            if not has_oil:
                tags.append('Oil-Free')
            if not has_irritant:
                tags.append('Sensitive Skin Friendly')
            
            print(f"   Tags: {', '.join(tags)}")
    
    else:
        print(f"❌ Failed to get products: {response.status_code}")

def main():
    """Run debug"""
    print("🚀 Debugging Ingredients and Tag Detection")
    print("=" * 60)
    
    try:
        debug_ingredients()
        
        print("\n" + "=" * 60)
        print("✅ Debug completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8080")
    except Exception as e:
        print(f"❌ Debug failed with error: {e}")

if __name__ == "__main__":
    main()
