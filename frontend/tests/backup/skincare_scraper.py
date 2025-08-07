#!/usr/bin/env python3
"""
Skincare Product Web Scraper
Scrapes skincare products from multiple sources and injects them into the database via API
"""

import requests
import json
import time
import random
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import mysql.connector
from mysql.connector import Error
import logging
from typing import List, Dict, Optional
import argparse
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SkincareScraper:
    def __init__(self, api_base_url: str = "http://localhost:8080/api", 
                 db_config: Optional[Dict] = None):
        self.api_base_url = api_base_url
        self.db_config = db_config or {
            'host': 'localhost',
            'port': 3306,
            'database': 'skincare_db',
            'user': 'root',
            'password': ''
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def scrape_incidecoder(self, max_pages: int = 10) -> List[Dict]:
        """Scrape products from INCIDecoder"""
        products = []
        base_url = "https://incidecoder.com"
        
        # Popular brands to scrape
        brands = [
            "the-ordinary", "cerave", "la-roche-posay", "neutrogena", 
            "paulas-choice", "skinceuticals", "clinique", "kiehls",
            "innisfree", "cosrx", "laneige", "etude-house", "numbuzin",
            "vt-cosmetics", "aprilskin", "the-saem", "neogen", "amplen"
        ]
        
        for brand in brands:
            try:
                logger.info(f"Scraping brand: {brand}")
                brand_url = f"{base_url}/brands/{brand}"
                
                response = self.session.get(brand_url)
                if response.status_code != 200:
                    continue
                    
                soup = BeautifulSoup(response.content, 'html.parser')
                product_links = soup.find_all('a', href=re.compile(r'/products/'))
                
                for link in product_links[:20]:  # Limit per brand
                    product_url = urljoin(base_url, link['href'])
                    product_data = self._scrape_incidecoder_product(product_url)
                    if product_data:
                        products.append(product_data)
                        time.sleep(random.uniform(1, 3))  # Be respectful
                        
            except Exception as e:
                logger.error(f"Error scraping brand {brand}: {e}")
                
        return products
    
    def _scrape_incidecoder_product(self, url: str) -> Optional[Dict]:
        """Scrape individual product from INCIDecoder"""
        try:
            response = self.session.get(url)
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product name
            name_elem = soup.find('h1')
            if not name_elem:
                return None
            name = name_elem.get_text(strip=True)
            
            # Extract brand
            brand_elem = soup.find('a', href=re.compile(r'/brands/'))
            brand = brand_elem.get_text(strip=True) if brand_elem else "Unknown"
            
            # Extract ingredients
            ingredients_section = soup.find('div', {'id': 'ingredients'})
            ingredients_list = ""
            if ingredients_section:
                ingredients = ingredients_section.find_all('a', href=re.compile(r'/ingredients/'))
                ingredients_list = ", ".join([ing.get_text(strip=True) for ing in ingredients])
            
            # Extract star ingredients (first 3-5 ingredients)
            star_ingredients = ""
            if ingredients_list:
                all_ingredients = [ing.strip() for ing in ingredients_list.split(',')]
                star_ingredients = ", ".join(all_ingredients[:5])
            
            # Determine product type from name
            product_type = self._determine_product_type(name)
            
            # Generate random price (you can modify this logic)
            price = random.randint(500, 5000)
            
            return {
                'name': name,
                'brand': brand,
                'ingredientsList': ingredients_list,
                'starIngredients': star_ingredients,
                'productType': product_type,
                'price': price
            }
            
        except Exception as e:
            logger.error(f"Error scraping product {url}: {e}")
            return None
    
    def scrape_sephora(self, max_pages: int = 5) -> List[Dict]:
        """Scrape products from Sephora (basic implementation)"""
        products = []
        base_url = "https://www.sephora.com"
        
        # Sephora skincare categories
        categories = [
            "/shop/skincare-cleansers",
            "/shop/skincare-moisturizers", 
            "/shop/skincare-serums",
            "/shop/skincare-sunscreen"
        ]
        
        for category in categories:
            try:
                logger.info(f"Scraping Sephora category: {category}")
                category_url = base_url + category
                
                response = self.session.get(category_url)
                if response.status_code != 200:
                    continue
                    
                soup = BeautifulSoup(response.content, 'html.parser')
                product_links = soup.find_all('a', href=re.compile(r'/product/'))
                
                for link in product_links[:10]:  # Limit per category
                    product_url = urljoin(base_url, link['href'])
                    product_data = self._scrape_sephora_product(product_url)
                    if product_data:
                        products.append(product_data)
                        time.sleep(random.uniform(2, 4))
                        
            except Exception as e:
                logger.error(f"Error scraping Sephora category {category}: {e}")
                
        return products
    
    def _scrape_sephora_product(self, url: str) -> Optional[Dict]:
        """Scrape individual product from Sephora"""
        try:
            response = self.session.get(url)
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product name
            name_elem = soup.find('h1') or soup.find('span', {'data-at': 'product_name'})
            if not name_elem:
                return None
            name = name_elem.get_text(strip=True)
            
            # Extract brand
            brand_elem = soup.find('a', href=re.compile(r'/brand/')) or soup.find('span', {'data-at': 'brand_name'})
            brand = brand_elem.get_text(strip=True) if brand_elem else "Unknown"
            
            # Extract price
            price_elem = soup.find('span', {'data-at': 'price'})
            price = 0
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'\$?(\d+(?:\.\d{2})?)', price_text)
                if price_match:
                    price = int(float(price_match.group(1)) * 100)  # Convert to cents
            
            # For Sephora, we'll need to get ingredients from product description
            # This is a simplified version
            ingredients_list = ""
            star_ingredients = ""
            
            # Determine product type
            product_type = self._determine_product_type(name)
            
            return {
                'name': name,
                'brand': brand,
                'ingredientsList': ingredients_list,
                'starIngredients': star_ingredients,
                'productType': product_type,
                'price': price
            }
            
        except Exception as e:
            logger.error(f"Error scraping Sephora product {url}: {e}")
            return None
    
    def scrape_ulta(self, max_pages: int = 5) -> List[Dict]:
        """Scrape products from Ulta Beauty"""
        products = []
        base_url = "https://www.ulta.com"
        
        # Ulta skincare categories
        categories = [
            "/shop/skincare/cleansers",
            "/shop/skincare/moisturizers",
            "/shop/skincare/serums",
            "/shop/skincare/sunscreen"
        ]
        
        for category in categories:
            try:
                logger.info(f"Scraping Ulta category: {category}")
                category_url = base_url + category
                
                response = self.session.get(category_url)
                if response.status_code != 200:
                    continue
                    
                soup = BeautifulSoup(response.content, 'html.parser')
                product_links = soup.find_all('a', href=re.compile(r'/product/'))
                
                for link in product_links[:10]:
                    product_url = urljoin(base_url, link['href'])
                    product_data = self._scrape_ulta_product(product_url)
                    if product_data:
                        products.append(product_data)
                        time.sleep(random.uniform(2, 4))
                        
            except Exception as e:
                logger.error(f"Error scraping Ulta category {category}: {e}")
                
        return products
    
    def _scrape_ulta_product(self, url: str) -> Optional[Dict]:
        """Scrape individual product from Ulta"""
        try:
            response = self.session.get(url)
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product name
            name_elem = soup.find('h1') or soup.find('span', {'class': 'ProductDetail__title'})
            if not name_elem:
                return None
            name = name_elem.get_text(strip=True)
            
            # Extract brand
            brand_elem = soup.find('a', href=re.compile(r'/brand/')) or soup.find('span', {'class': 'ProductDetail__brand'})
            brand = brand_elem.get_text(strip=True) if brand_elem else "Unknown"
            
            # Extract price
            price_elem = soup.find('span', {'class': 'ProductPricing__price'})
            price = 0
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'\$?(\d+(?:\.\d{2})?)', price_text)
                if price_match:
                    price = int(float(price_match.group(1)) * 100)
            
            # Simplified ingredients extraction
            ingredients_list = ""
            star_ingredients = ""
            
            product_type = self._determine_product_type(name)
            
            return {
                'name': name,
                'brand': brand,
                'ingredientsList': ingredients_list,
                'starIngredients': star_ingredients,
                'productType': product_type,
                'price': price
            }
            
        except Exception as e:
            logger.error(f"Error scraping Ulta product {url}: {e}")
            return None
    
    def _determine_product_type(self, name: str) -> str:
        """Determine product type based on product name"""
        name_lower = name.lower()
        
        type_keywords = {
            'Cleanser': ['cleanser', 'wash', 'foam', 'gel cleanser', 'cleansing'],
            'Toner': ['toner', 'toning'],
            'Serum': ['serum', 'booster'],
            'Moisturizer': ['moisturizer', 'cream', 'lotion', 'hydrating'],
            'Sunscreen': ['sunscreen', 'spf', 'sun protection'],
            'Mask': ['mask', 'sheet mask'],
            'Treatment': ['treatment', 'spot treatment', 'acne'],
            'Eye Cream': ['eye', 'eye cream', 'eye gel'],
            'Essence': ['essence'],
            'Ampoule': ['ampoule', 'ampule'],
            'Lip Care': ['lip', 'lip balm', 'lip treatment']
        }
        
        for product_type, keywords in type_keywords.items():
            if any(keyword in name_lower for keyword in keywords):
                return product_type
        
        return 'Other'
    
    def add_product_via_api(self, product: Dict) -> bool:
        """Add product to database via API"""
        try:
            response = self.session.post(
                f"{self.api_base_url}/products",
                json=product,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201 or response.status_code == 200:
                logger.info(f"Successfully added product: {product['name']}")
                return True
            else:
                logger.error(f"Failed to add product {product['name']}: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error adding product via API: {e}")
            return False
    
    def add_product_via_database(self, product: Dict) -> bool:
        """Add product directly to database"""
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            query = """
            INSERT INTO products (name, brand, ingredients_list, star_ingredients, product_type, price)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            values = (
                product['name'],
                product['brand'],
                product['ingredientsList'],
                product['starIngredients'],
                product['productType'],
                product['price']
            )
            
            cursor.execute(query, values)
            connection.commit()
            
            logger.info(f"Successfully added product to database: {product['name']}")
            return True
            
        except Error as e:
            logger.error(f"Database error: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def run_scraper(self, sources: List[str] = None, method: str = 'api') -> None:
        """Run the scraper with specified sources and method"""
        if sources is None:
            sources = ['incidecoder', 'sephora', 'ulta']
        
        all_products = []
        
        for source in sources:
            logger.info(f"Starting to scrape from {source}")
            
            if source == 'incidecoder':
                products = self.scrape_incidecoder()
            elif source == 'sephora':
                products = self.scrape_sephora()
            elif source == 'ulta':
                products = self.scrape_ulta()
            else:
                logger.warning(f"Unknown source: {source}")
                continue
            
            all_products.extend(products)
            logger.info(f"Scraped {len(products)} products from {source}")
        
        logger.info(f"Total products scraped: {len(all_products)}")
        
        # Add products to database
        success_count = 0
        for product in all_products:
            if method == 'api':
                if self.add_product_via_api(product):
                    success_count += 1
            elif method == 'database':
                if self.add_product_via_database(product):
                    success_count += 1
            
            time.sleep(random.uniform(0.5, 1.5))  # Rate limiting
        
        logger.info(f"Successfully added {success_count} products to database")

def main():
    parser = argparse.ArgumentParser(description='Skincare Product Scraper')
    parser.add_argument('--sources', nargs='+', 
                       choices=['incidecoder', 'sephora', 'ulta'],
                       default=['incidecoder'],
                       help='Sources to scrape from')
    parser.add_argument('--method', choices=['api', 'database'],
                       default='api',
                       help='Method to add products (api or database)')
    parser.add_argument('--api-url', default='http://localhost:8080/api',
                       help='API base URL')
    parser.add_argument('--db-host', default='localhost',
                       help='Database host')
    parser.add_argument('--db-port', type=int, default=3306,
                       help='Database port')
    parser.add_argument('--db-name', default='skincare_db',
                       help='Database name')
    parser.add_argument('--db-user', default='root',
                       help='Database user')
    parser.add_argument('--db-password', default='',
                       help='Database password')
    
    args = parser.parse_args()
    
    # Configure database connection
    db_config = {
        'host': args.db_host,
        'port': args.db_port,
        'database': args.db_name,
        'user': args.db_user,
        'password': args.db_password
    }
    
    # Create scraper instance
    scraper = SkincareScraper(
        api_base_url=args.api_url,
        db_config=db_config
    )
    
    # Run scraper
    scraper.run_scraper(sources=args.sources, method=args.method)

if __name__ == "__main__":
    main()
