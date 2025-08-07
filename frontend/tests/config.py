#!/usr/bin/env python3
"""
Test configuration and utilities for all test scripts
"""

import requests
import json
import time
from typing import Dict, List, Any

# Configuration
API_BASE_URL = "http://localhost:8080/api/products"
BRANDS_API_URL = "http://localhost:8080/api/products/brands"

# Test utilities
def make_api_request(url: str, params: Dict = None) -> Dict:
    """Make API request and return response"""
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

def print_test_result(test_name: str, passed: bool, details: str = ""):
    """Print formatted test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"   Details: {details}")
    print()

def test_api_connection():
    """Test basic API connectivity"""
    print("Testing API connection...")
    response = make_api_request(API_BASE_URL, {"page": 1, "limit": 5})
    if response:
        print_test_result("API Connection", True, f"Retrieved {len(response.get('products', []))} products")
        return True
    else:
        print_test_result("API Connection", False, "Could not connect to API")
        return False

def get_all_products():
    """Get all products for testing"""
    all_products = []
    page = 1
    
    while True:
        response = make_api_request(API_BASE_URL, {"page": page, "limit": 100})
        if not response:
            break
        
        # Handle both response formats: object with 'products' key or direct list
        if isinstance(response, dict) and 'products' in response:
            products = response['products']
        elif isinstance(response, list):
            products = response
        else:
            break
        
        if not products:
            break
        
        all_products.extend(products)
        
        if len(products) < 100:  # Last page
            break
        page += 1
    
    return all_products
