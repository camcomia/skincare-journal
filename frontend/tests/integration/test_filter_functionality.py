import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import make_api_request, print_test_result, get_all_products, API_BASE_URL, BRANDS_API_URL

def parse_api_response(response):
    """Parse API response and return products and total count"""
    if isinstance(response, dict):
        products = response.get('products', [])
        total = response.get('total', 0)
    elif isinstance(response, list):
        products = response
        total = len(response)
    else:
        products = []
        total = 0
    return products, total

def test_tag_filters():
    """Test all tag filters (alcohol-free, fragrance-free, oil-free, sensitive skin friendly)"""
    print("Testing tag filters...")
    
    # Test each tag individually
    tags_to_test = ['alcohol-free', 'fragrance-free', 'oil-free', 'sensitive skin friendly']
    
    for tag in tags_to_test:
        print(f"\nTesting {tag} filter...")
        
        # Get products with this tag filter
        response = make_api_request(API_BASE_URL, {
            "page": 1,
            "limit": 50,
            "tags": tag
        })
        
        if not response:
            print_test_result(f"{tag} filter", False, "API request failed")
            continue
        
        products, total = parse_api_response(response)
        
        print(f"Found {len(products)} products with {tag} filter (total: {total})")
        
        # Verify that returned products actually match the tag
        if products:
            # Check first few products to verify they match the tag
            for i, product in enumerate(products[:3]):  # Check first 3 products
                ingredients = product.get('ingredientsList', '').lower()
                name = product.get('name', '').lower()
                
                if tag == 'alcohol-free':
                    has_alcohol = any(word in ingredients for word in ['alcohol', 'ethanol', 'denatured'])
                    if has_alcohol:
                        print_test_result(f"{tag} filter - product {i+1}", False, 
                                        f"Product '{product.get('name')}' has alcohol but was returned")
                        continue
                
                elif tag == 'fragrance-free':
                    has_fragrance = any(word in ingredients for word in ['fragrance', 'parfum', 'perfume'])
                    if has_fragrance:
                        print_test_result(f"{tag} filter - product {i+1}", False,
                                        f"Product '{product.get('name')}' has fragrance but was returned")
                        continue
                
                elif tag == 'oil-free':
                    has_oil = any(word in ingredients or word in name for word in 
                                ['oil', 'argan', 'squalane', 'jojoba', 'coconut', 'olive'])
                    if has_oil:
                        print_test_result(f"{tag} filter - product {i+1}", False,
                                        f"Product '{product.get('name')}' has oil but was returned")
                        continue
                
                elif tag == 'sensitive skin friendly':
                    has_irritants = any(word in ingredients for word in 
                                      ['alcohol', 'fragrance', 'menthol', 'peppermint'])
                    if has_irritants:
                        print_test_result(f"{tag} filter - product {i+1}", False,
                                        f"Product '{product.get('name')}' has irritants but was returned")
                        continue
            
            print_test_result(f"{tag} filter", True, f"Found {len(products)} products")
        else:
            print_test_result(f"{tag} filter", True, "No products found (this may be correct)")

def test_product_type_filter():
    """Test product type filtering"""
    print("\nTesting product type filter...")
    
    # Test a few common product types
    product_types = ['Cleanser', 'Toner', 'Serum', 'Moisturizer']
    
    for product_type in product_types:
        response = make_api_request(API_BASE_URL, {
            "page": 1,
            "limit": 20,
            "productType": product_type
        })
        
        if not response:
            print_test_result(f"Product type filter: {product_type}", False, "API request failed")
            continue
        
        products, total = parse_api_response(response)
        
        print(f"Found {len(products)} products with type '{product_type}' (total: {total})")
        
        # Verify all returned products have the correct type
        if products:
            for product in products:
                if product.get('productType') != product_type:
                    print_test_result(f"Product type filter: {product_type}", False,
                                    f"Product '{product.get('name')}' has type '{product.get('productType')}' but should be '{product_type}'")
                    break
            else:
                print_test_result(f"Product type filter: {product_type}", True, f"Found {len(products)} products")
        else:
            print_test_result(f"Product type filter: {product_type}", True, "No products found (this may be correct)")

def test_brand_filter():
    """Test brand filtering"""
    print("\nTesting brand filter...")
    
    # First get available brands
    brands_response = make_api_request(BRANDS_API_URL)
    if not brands_response:
        print_test_result("Brand filter", False, "Could not fetch brands")
        return
    
    # Handle brands response format
    if isinstance(brands_response, dict):
        brands = brands_response.get('brands', [])
    elif isinstance(brands_response, list):
        brands = brands_response
    else:
        brands = []
    if not brands:
        print_test_result("Brand filter", False, "No brands available")
        return
    
    # Test first few brands
    for brand in brands[:3]:  # Test first 3 brands
        response = make_api_request(API_BASE_URL, {
            "page": 1,
            "limit": 20,
            "brand": brand
        })
        
        if not response:
            print_test_result(f"Brand filter: {brand}", False, "API request failed")
            continue
        
        products, total = parse_api_response(response)
        
        print(f"Found {len(products)} products from brand '{brand}' (total: {total})")
        
        # Verify all returned products have the correct brand
        if products:
            for product in products:
                if product.get('brand') != brand:
                    print_test_result(f"Brand filter: {brand}", False,
                                    f"Product '{product.get('name')}' has brand '{product.get('brand')}' but should be '{brand}'")
                    break
            else:
                print_test_result(f"Brand filter: {brand}", True, f"Found {len(products)} products")
        else:
            print_test_result(f"Brand filter: {brand}", True, "No products found (this may be correct)")

def test_search_functionality():
    """Test search functionality"""
    print("\nTesting search functionality...")
    
    # Get all products to find some search terms
    all_products = get_all_products()
    if not all_products:
        print_test_result("Search functionality", False, "Could not get products for testing")
        return
    
    # Test search with product names
    for product in all_products[:3]:  # Test first 3 products
        product_name = product.get('name', '')
        if not product_name:
            continue
        
        # Search for first word of product name
        search_term = product_name.split()[0]
        
        response = make_api_request(API_BASE_URL, {
            "page": 1,
            "limit": 20,
            "search": search_term
        })
        
        if not response:
            print_test_result(f"Search: {search_term}", False, "API request failed")
            continue
        
        products, total = parse_api_response(response)
        
        print(f"Search '{search_term}' found {len(products)} products (total: {total})")
        
        # Verify that at least one product contains the search term
        found_match = False
        for product in products:
            if search_term.lower() in product.get('name', '').lower():
                found_match = True
                break
        
        if found_match:
            print_test_result(f"Search: {search_term}", True, f"Found {len(products)} products")
        else:
            print_test_result(f"Search: {search_term}", False, "No matching products found")

def test_sort_functionality():
    """Test sorting functionality"""
    print("\nTesting sort functionality...")
    
    sort_options = ['name', 'name-desc', 'price', 'price-desc', 'brand']
    
    for sort_by in sort_options:
        response = make_api_request(API_BASE_URL, {
            "page": 1,
            "limit": 10,
            "sortBy": sort_by
        })
        
        if not response:
            print_test_result(f"Sort: {sort_by}", False, "API request failed")
            continue
        
        products, _ = parse_api_response(response)
        
        if len(products) < 2:
            print_test_result(f"Sort: {sort_by}", True, "Not enough products to test sorting")
            continue
        
        # Verify sorting order
        is_sorted = True
        for i in range(len(products) - 1):
            current = products[i]
            next_product = products[i + 1]
            
            if sort_by == 'name':
                if current.get('name', '') > next_product.get('name', ''):
                    is_sorted = False
                    break
            elif sort_by == 'name-desc':
                if current.get('name', '') < next_product.get('name', ''):
                    is_sorted = False
                    break
            elif sort_by == 'price':
                if current.get('price', 0) > next_product.get('price', 0):
                    is_sorted = False
                    break
            elif sort_by == 'price-desc':
                if current.get('price', 0) < next_product.get('price', 0):
                    is_sorted = False
                    break
            elif sort_by == 'brand':
                if current.get('brand', '') > next_product.get('brand', ''):
                    is_sorted = False
                    break
        
        if is_sorted:
            print_test_result(f"Sort: {sort_by}", True, f"Products correctly sorted")
        else:
            print_test_result(f"Sort: {sort_by}", False, "Products not correctly sorted")

def test_combined_filters():
    """Test combining multiple filters"""
    print("\nTesting combined filters...")
    
    # Test combining product type and tag filter
    response = make_api_request(API_BASE_URL, {
        "page": 1,
        "limit": 20,
        "productType": "Cleanser",
        "tags": "fragrance-free"
    })
    
    if not response:
        print_test_result("Combined filters", False, "API request failed")
        return
    
    products, total = parse_api_response(response)
    
    print(f"Combined filter (Cleanser + fragrance-free) found {len(products)} products (total: {total})")
    
    # Verify all products match both filters
    if products:
        for product in products:
            # Check product type
            if product.get('productType') != 'Cleanser':
                print_test_result("Combined filters", False,
                                f"Product '{product.get('name')}' has wrong type")
                break
            
            # Check fragrance-free
            ingredients = product.get('ingredientsList', '').lower()
            if 'fragrance' in ingredients or 'parfum' in ingredients or 'perfume' in ingredients:
                print_test_result("Combined filters", False,
                                f"Product '{product.get('name')}' has fragrance but should be fragrance-free")
                break
        else:
            print_test_result("Combined filters", True, f"Found {len(products)} products matching both filters")
    else:
        print_test_result("Combined filters", True, "No products found (this may be correct)")

def run_all_filter_tests():
    """Run all filter tests"""
    print("🧪 Starting Filter Functionality Tests")
    print("=" * 50)
    
    test_tag_filters()
    test_product_type_filter()
    test_brand_filter()
    test_search_functionality()
    test_sort_functionality()
    test_combined_filters()
    
    print("=" * 50)
    print("✅ Filter functionality tests completed!")

if __name__ == "__main__":
    run_all_filter_tests()
