#!/usr/bin/env python3
"""
Comprehensive integration tests for the API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import TestConfig, TestLogger, validate_product_data, check_oil_detection
import time

class APIIntegrationTests:
    """Integration tests for the API"""
    
    def __init__(self):
        self.logger = TestLogger("API Integration Tests")
    
    def test_basic_api_connectivity(self):
        """Test basic API connectivity"""
        try:
            response = TestConfig.make_request("", {"page": 1, "limit": 5})
            if TestConfig.check_response(response, "Basic API Connectivity"):
                data = response.json()
                products = data.get('products', [])
                self.logger.log_success("Basic API Connectivity", f"Found {len(products)} products")
                return True
            return False
        except Exception as e:
            self.logger.log_failure("Basic API Connectivity", f"Exception: {e}")
            return False
    
    def test_search_functionality(self):
        """Test search functionality"""
        search_terms = ["ordinary", "garnier", "oil", "serum", "xyz123"]
        
        for term in search_terms:
            try:
                start_time = time.time()
                response = TestConfig.make_request("", {"search": term, "page": 1, "limit": 10})
                end_time = time.time()
                
                if TestConfig.check_response(response, f"Search '{term}'"):
                    data = response.json()
                    products = data.get('products', [])
                    response_time = end_time - start_time
                    
                    # Validate results
                    if term == "xyz123":
                        if len(products) == 0:
                            self.logger.log_success(f"Search '{term}'", f"No results (correct) in {TestConfig.format_time(response_time)}")
                        else:
                            self.logger.log_failure(f"Search '{term}'", f"Found {len(products)} unexpected results")
                    else:
                        # Check if results are relevant
                        relevant_results = 0
                        for product in products:
                            name = product.get('name', '').lower()
                            brand = product.get('brand', '').lower()
                            ingredients = product.get('ingredientsList', '').lower()
                            
                            if term.lower() in name or term.lower() in brand or term.lower() in ingredients:
                                relevant_results += 1
                        
                        if relevant_results == len(products) or len(products) == 0:
                            self.logger.log_success(f"Search '{term}'", f"{len(products)} results in {TestConfig.format_time(response_time)}")
                        else:
                            self.logger.log_warning(f"Search '{term}'", f"{relevant_results}/{len(products)} relevant results")
                else:
                    self.logger.log_failure(f"Search '{term}'", "Request failed")
                    
            except Exception as e:
                self.logger.log_failure(f"Search '{term}'", f"Exception: {e}")
    
    def test_brand_filtering(self):
        """Test brand filtering"""
        brands = ["The Ordinary", "Garnier", "COSRX"]
        
        for brand in brands:
            try:
                response = TestConfig.make_request("", {"brand": brand, "page": 1, "limit": 10})
                
                if TestConfig.check_response(response, f"Brand filter '{brand}'"):
                    data = response.json()
                    products = data.get('products', [])
                    
                    # Validate all results are from the specified brand
                    correct_brand_count = 0
                    for product in products:
                        if product.get('brand') == brand:
                            correct_brand_count += 1
                    
                    if correct_brand_count == len(products):
                        self.logger.log_success(f"Brand filter '{brand}'", f"{len(products)} products")
                    else:
                        self.logger.log_failure(f"Brand filter '{brand}'", f"{correct_brand_count}/{len(products)} correct")
                else:
                    self.logger.log_failure(f"Brand filter '{brand}'", "Request failed")
                    
            except Exception as e:
                self.logger.log_failure(f"Brand filter '{brand}'", f"Exception: {e}")
    
    def test_tag_filtering(self):
        """Test tag filtering"""
        tags = ["Alcohol-Free", "Fragrance-Free", "Oil-Free", "Sensitive Skin Friendly"]
        
        for tag in tags:
            try:
                response = TestConfig.make_request("", {"tags": tag, "page": 1, "limit": 10})
                
                if TestConfig.check_response(response, f"Tag filter '{tag}'"):
                    data = response.json()
                    products = data.get('products', [])
                    
                    # Special validation for Oil-Free tag
                    if tag == "Oil-Free":
                        oil_products_in_results = []
                        for product in products:
                            name = product.get('name', '')
                            ingredients = product.get('ingredientsList', '')
                            oil_check = check_oil_detection(name, ingredients)
                            
                            if not oil_check['is_oil_free']:
                                oil_products_in_results.append(name)
                        
                        if oil_products_in_results:
                            self.logger.log_failure(f"Tag filter '{tag}'", f"Found products with oils: {oil_products_in_results[:3]}")
                        else:
                            self.logger.log_success(f"Tag filter '{tag}'", f"{len(products)} products")
                    else:
                        self.logger.log_success(f"Tag filter '{tag}'", f"{len(products)} products")
                else:
                    self.logger.log_failure(f"Tag filter '{tag}'", "Request failed")
                    
            except Exception as e:
                self.logger.log_failure(f"Tag filter '{tag}'", f"Exception: {e}")
    
    def test_sorting_functionality(self):
        """Test sorting functionality"""
        sort_options = ["name", "name-desc", "price", "price-desc", "brand"]
        
        for sort_by in sort_options:
            try:
                response = TestConfig.make_request("", {"sortBy": sort_by, "page": 1, "limit": 5})
                
                if TestConfig.check_response(response, f"Sort '{sort_by}'"):
                    data = response.json()
                    products = data.get('products', [])
                    
                    if len(products) >= 2:
                        # Basic validation that sorting worked
                        if sort_by == "name":
                            # Check if first product name comes before second
                            if products[0]['name'].lower() <= products[1]['name'].lower():
                                self.logger.log_success(f"Sort '{sort_by}'", "Ordered correctly")
                            else:
                                self.logger.log_warning(f"Sort '{sort_by}'", "Order may be incorrect")
                        elif sort_by == "price":
                            # Check if first product price is less than or equal to second
                            price1 = products[0].get('price', 0) or 0
                            price2 = products[1].get('price', 0) or 0
                            if price1 <= price2:
                                self.logger.log_success(f"Sort '{sort_by}'", "Ordered correctly")
                            else:
                                self.logger.log_warning(f"Sort '{sort_by}'", "Order may be incorrect")
                        else:
                            self.logger.log_success(f"Sort '{sort_by}'", f"{len(products)} products")
                    else:
                        self.logger.log_success(f"Sort '{sort_by}'", f"{len(products)} products")
                else:
                    self.logger.log_failure(f"Sort '{sort_by}'", "Request failed")
                    
            except Exception as e:
                self.logger.log_failure(f"Sort '{sort_by}'", f"Exception: {e}")
    
    def test_combined_filters(self):
        """Test combined filters"""
        test_cases = [
            {"search": "ordinary", "brand": "The Ordinary", "productType": "Other"},
            {"search": "oil", "tags": "Oil-Free"},
            {"brand": "The Ordinary", "sortBy": "name"},
            {"search": "ordinary", "tags": "Alcohol-Free", "sortBy": "price"}
        ]
        
        for i, filters in enumerate(test_cases, 1):
            try:
                filters["page"] = 1
                filters["limit"] = 5
                
                response = TestConfig.make_request("", filters)
                
                if TestConfig.check_response(response, f"Combined filters {i}"):
                    data = response.json()
                    products = data.get('products', [])
                    self.logger.log_success(f"Combined filters {i}", f"{len(products)} products")
                else:
                    self.logger.log_failure(f"Combined filters {i}", "Request failed")
                    
            except Exception as e:
                self.logger.log_failure(f"Combined filters {i}", f"Exception: {e}")
    
    def test_pagination(self):
        """Test pagination functionality"""
        try:
            # Test first page
            response1 = TestConfig.make_request("", {"page": 1, "limit": 3})
            
            if TestConfig.check_response(response1, "Pagination page 1"):
                data1 = response1.json()
                products1 = data1.get('products', [])
                
                # Test second page
                response2 = TestConfig.make_request("", {"page": 2, "limit": 3})
                
                if TestConfig.check_response(response2, "Pagination page 2"):
                    data2 = response2.json()
                    products2 = data2.get('products', [])
                    
                    # Check that pages have different products
                    if len(products1) > 0 and len(products2) > 0:
                        if products1[0]['id'] != products2[0]['id']:
                            self.logger.log_success("Pagination", "Pages have different products")
                        else:
                            self.logger.log_warning("Pagination", "Pages may have duplicate products")
                    else:
                        self.logger.log_success("Pagination", f"Page 1: {len(products1)}, Page 2: {len(products2)}")
                else:
                    self.logger.log_failure("Pagination", "Page 2 request failed")
            else:
                self.logger.log_failure("Pagination", "Page 1 request failed")
                
        except Exception as e:
            self.logger.log_failure("Pagination", f"Exception: {e}")
    
    def test_performance(self):
        """Test API performance"""
        test_queries = [
            {"page": 1, "limit": 10},
            {"search": "ordinary", "page": 1, "limit": 5},
            {"brand": "The Ordinary", "page": 1, "limit": 10},
            {"tags": "Oil-Free", "page": 1, "limit": 10},
            {"sortBy": "name", "page": 1, "limit": 10}
        ]
        
        total_time = 0
        successful_queries = 0
        
        for i, query in enumerate(test_queries, 1):
            try:
                start_time = time.time()
                response = TestConfig.make_request("", query)
                end_time = time.time()
                
                if TestConfig.check_response(response, f"Performance test {i}"):
                    query_time = end_time - start_time
                    total_time += query_time
                    successful_queries += 1
                    
                    if query_time < 0.1:
                        self.logger.log_success(f"Performance test {i}", f"{TestConfig.format_time(query_time)}")
                    else:
                        self.logger.log_warning(f"Performance test {i}", f"{TestConfig.format_time(query_time)} (slow)")
                else:
                    self.logger.log_failure(f"Performance test {i}", "Request failed")
                    
            except Exception as e:
                self.logger.log_failure(f"Performance test {i}", f"Exception: {e}")
        
        if successful_queries > 0:
            avg_time = total_time / successful_queries
            self.logger.log_info(f"Average response time: {TestConfig.format_time(avg_time)}")
    
    def test_data_validation(self):
        """Test that returned data has correct structure"""
        try:
            response = TestConfig.make_request("", {"page": 1, "limit": 10})
            
            if TestConfig.check_response(response, "Data validation"):
                data = response.json()
                products = data.get('products', [])
                
                valid_products = 0
                for product in products:
                    if validate_product_data(product):
                        valid_products += 1
                    else:
                        self.logger.log_warning("Data validation", f"Invalid product: {product.get('name', 'Unknown')}")
                
                if valid_products == len(products):
                    self.logger.log_success("Data validation", f"All {len(products)} products have valid structure")
                else:
                    self.logger.log_failure("Data validation", f"{valid_products}/{len(products)} products have valid structure")
            else:
                self.logger.log_failure("Data validation", "Request failed")
                
        except Exception as e:
            self.logger.log_failure("Data validation", f"Exception: {e}")
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Running API Integration Tests")
        print("=" * 60)
        
        # Run all test methods
        test_methods = [
            self.test_basic_api_connectivity,
            self.test_search_functionality,
            self.test_brand_filtering,
            self.test_tag_filtering,
            self.test_sorting_functionality,
            self.test_combined_filters,
            self.test_pagination,
            self.test_performance,
            self.test_data_validation
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.logger.log_failure(test_method.__name__, f"Unexpected error: {e}")
        
        self.logger.summary()

def main():
    """Run integration tests"""
    try:
        tests = APIIntegrationTests()
        tests.run_all_tests()
    except Exception as e:
        print(f"❌ Test suite failed: {e}")

if __name__ == "__main__":
    main()
