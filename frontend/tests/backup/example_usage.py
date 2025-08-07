#!/usr/bin/env python3
"""
Example usage of the skincare scraper
Demonstrates how to use the scraper programmatically with custom configurations
"""

from enhanced_scraper import EnhancedSkincareScraper
from skincare_scraper import SkincareScraper
import json
import time

def example_basic_scraper():
    """Example using the basic scraper"""
    print("=== Basic Scraper Example ===")
    
    # Create scraper instance
    scraper = SkincareScraper(
        api_base_url="http://localhost:8080/api",
        db_config={
            'host': 'localhost',
            'port': 3306,
            'database': 'skincare_db',
            'user': 'root',
            'password': ''
        }
    )
    
    # Scrape a small number of products for testing
    scraper.run_scraper(
        sources=['incidecoder'],
        method='api',
        max_products=5
    )

def example_enhanced_scraper():
    """Example using the enhanced scraper with Selenium"""
    print("=== Enhanced Scraper Example ===")
    
    # Create enhanced scraper instance
    scraper = EnhancedSkincareScraper(
        api_base_url="http://localhost:8080/api",
        db_config={
            'host': 'localhost',
            'port': 3306,
            'database': 'skincare_db',
            'user': 'root',
            'password': ''
        },
        use_selenium=True
    )
    
    try:
        # Scrape from multiple sources
        scraper.run_scraper(
            sources=['incidecoder', 'sephora'],
            method='api',
            max_products=10
        )
    finally:
        # Cleanup Selenium driver
        if scraper.driver:
            scraper.driver.quit()

def example_custom_scraping():
    """Example of custom scraping with manual product processing"""
    print("=== Custom Scraping Example ===")
    
    scraper = EnhancedSkincareScraper(
        api_base_url="http://localhost:8080/api",
        use_selenium=False  # Use requests only for faster processing
    )
    
    # Scrape products without adding to database
    products = scraper.scrape_incidecoder_enhanced(max_products=5)
    
    print(f"Scraped {len(products)} products:")
    for i, product in enumerate(products, 1):
        print(f"\n{i}. {product['name']} by {product['brand']}")
        print(f"   Type: {product['productType']}")
        print(f"   Price: ${product['price']/100:.2f}")
        print(f"   Star Ingredients: {product['starIngredients']}")
        print(f"   Full Ingredients: {product['ingredientsList'][:100]}...")
    
    # Ask user if they want to add these products
    response = input("\nDo you want to add these products to your database? (y/n): ")
    if response.lower() == 'y':
        success_count = 0
        for product in products:
            if scraper.add_product_via_api(product):
                success_count += 1
            time.sleep(1)  # Rate limiting
        
        print(f"Successfully added {success_count} products to database!")

def example_database_insertion():
    """Example of direct database insertion"""
    print("=== Database Insertion Example ===")
    
    scraper = EnhancedSkincareScraper(
        api_base_url="http://localhost:8080/api",
        db_config={
            'host': 'localhost',
            'port': 3306,
            'database': 'skincare_db',
            'user': 'root',
            'password': ''  # Add your password here
        },
        use_selenium=False
    )
    
    # Scrape and add directly to database
    scraper.run_scraper(
        sources=['incidecoder'],
        method='database',  # Use direct database insertion
        max_products=3
    )

def example_save_to_json():
    """Example of saving scraped data to JSON file"""
    print("=== Save to JSON Example ===")
    
    scraper = EnhancedSkincareScraper(
        api_base_url="http://localhost:8080/api",
        use_selenium=False
    )
    
    # Scrape products
    products = scraper.scrape_incidecoder_enhanced(max_products=10)
    
    # Save to JSON file
    filename = f"scraped_products_{int(time.time())}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(products)} products to {filename}")
    
    # Display sample data
    if products:
        print("\nSample product data:")
        sample = products[0]
        print(json.dumps(sample, indent=2))

def main():
    """Main function to run examples"""
    print("Skincare Scraper Examples")
    print("=" * 40)
    
    examples = [
        ("Basic Scraper", example_basic_scraper),
        ("Enhanced Scraper", example_enhanced_scraper),
        ("Custom Scraping", example_custom_scraping),
        ("Database Insertion", example_database_insertion),
        ("Save to JSON", example_save_to_json)
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    print("\n0. Run all examples")
    
    try:
        choice = int(input("\nEnter your choice (0-5): "))
        
        if choice == 0:
            # Run all examples
            for name, func in examples:
                print(f"\n{'='*20} {name} {'='*20}")
                try:
                    func()
                except Exception as e:
                    print(f"Error in {name}: {e}")
                print()
        elif 1 <= choice <= len(examples):
            # Run specific example
            name, func = examples[choice - 1]
            print(f"\n{'='*20} {name} {'='*20}")
            func()
        else:
            print("Invalid choice!")
            
    except ValueError:
        print("Please enter a valid number!")
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
