#!/usr/bin/env python3
"""
Enhanced Skincare Product Web Scraper
Uses Selenium for better scraping capabilities and more sophisticated data extraction
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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedSkincareScraper:
    def __init__(self, api_base_url: str = "http://localhost:8080/api", 
                 db_config: Optional[Dict] = None, use_selenium: bool = True):
        self.api_base_url = api_base_url
        self.db_config = db_config or {
            'host': 'localhost',
            'port': 3306,
            'database': 'skincare_db',
            'user': 'root',
            'password': ''
        }
        self.use_selenium = use_selenium
        
        # Setup requests session
        self.session = requests.Session()
        ua = UserAgent()
        self.session.headers.update({
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Setup Selenium driver if needed
        self.driver = None
        if use_selenium:
            self._setup_selenium()
    
    def _setup_selenium(self):
        """Setup Selenium WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Selenium WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Selenium: {e}")
            self.use_selenium = False
    
    def __del__(self):
        """Cleanup Selenium driver"""
        if self.driver:
            self.driver.quit()
    
    def scrape_incidecoder_enhanced(self, max_products: int = 50) -> List[Dict]:
        """Enhanced scraping from INCIDecoder using Selenium"""
        products = []
        base_url = "https://incidecoder.com"
        
        # Popular brands with more comprehensive list
        brands = [
            "the-ordinary", "cerave", "la-roche-posay", "neutrogena", 
            "paulas-choice", "skinceuticals", "clinique", "kiehls",
            "innisfree", "cosrx", "laneige", "etude-house", "sk-ii",
            "estee-lauder", "lancome", "olay", "dove", "nivea",
            "aveeno", "eucerin", "cetaphil", "dermalogica"
        ]
        
        for brand in brands:
            if len(products) >= max_products:
                break
                
            try:
                logger.info(f"Scraping brand: {brand}")
                brand_url = f"{base_url}/brands/{brand}"
                
                if self.use_selenium and self.driver:
                    self.driver.get(brand_url)
                    time.sleep(random.uniform(2, 4))
                    
                    # Wait for products to load
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/products/']"))
                        )
                    except:
                        pass
                    
                    # Get all product links
                    product_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/products/']")
                    product_links = [elem.get_attribute('href') for elem in product_elements]
                else:
                    response = self.session.get(brand_url)
                    if response.status_code != 200:
                        continue
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    product_elements = soup.find_all('a', href=re.compile(r'/products/'))
                    product_links = [urljoin(base_url, elem['href']) for elem in product_elements]
                
                # Limit products per brand
                for link in product_links[:10]:
                    if len(products) >= max_products:
                        break
                        
                    product_data = self._scrape_incidecoder_product_enhanced(link)
                    if product_data:
                        products.append(product_data)
                        logger.info(f"Added product: {product_data['name']}")
                        time.sleep(random.uniform(1, 3))
                        
            except Exception as e:
                logger.error(f"Error scraping brand {brand}: {e}")
                
        return products
    
    def _scrape_incidecoder_product_enhanced(self, url: str) -> Optional[Dict]:
        """Enhanced scraping of individual product from INCIDecoder"""
        try:
            if self.use_selenium and self.driver:
                self.driver.get(url)
                time.sleep(random.uniform(2, 4))
                
                # Wait for page to load
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "h1"))
                    )
                except:
                    pass
                
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
            else:
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
            
            # Extract ingredients with better parsing
            ingredients_list = ""
            star_ingredients = ""
            
            # Try multiple selectors for ingredients
            ingredients_selectors = [
                'div#ingredients a[href*="/ingredients/"]',
                '.ingredients-list a[href*="/ingredients/"]',
                'div[class*="ingredient"] a[href*="/ingredients/"]'
            ]
            
            for selector in ingredients_selectors:
                ingredients = soup.select(selector)
                if ingredients:
                    ingredients_list = ", ".join([ing.get_text(strip=True) for ing in ingredients])
                    break
            
            # If no ingredients found, try alternative method
            if not ingredients_list:
                # Look for ingredients in text content
                ingredients_text = soup.get_text()
                ingredients_match = re.search(r'Ingredients[:\s]*(.*?)(?:\n|$)', ingredients_text, re.IGNORECASE)
                if ingredients_match:
                    ingredients_list = ingredients_match.group(1).strip()
            
            # Extract star ingredients (first 5-8 ingredients)
            if ingredients_list:
                all_ingredients = [ing.strip() for ing in ingredients_list.split(',')]
                # Filter out common filler ingredients for star ingredients
                star_ingredients_list = []
                for ing in all_ingredients[:8]:
                    ing_lower = ing.lower()
                    if not any(filler in ing_lower for filler in ['water', 'aqua', 'glycerin', 'propylene glycol']):
                        star_ingredients_list.append(ing)
                    if len(star_ingredients_list) >= 5:
                        break
                star_ingredients = ", ".join(star_ingredients_list)
            
            # Determine product type with enhanced logic
            product_type = self._determine_product_type_enhanced(name, ingredients_list)
            
            # Generate realistic price based on brand and product type
            price = self._generate_realistic_price(brand, product_type)
            
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
    
    def scrape_sephora_enhanced(self, max_products: int = 30) -> List[Dict]:
        """Enhanced scraping from Sephora"""
        products = []
        base_url = "https://www.sephora.com"
        
        # Sephora skincare categories with more specific URLs
        categories = [
            "/shop/skincare-cleansers",
            "/shop/skincare-moisturizers", 
            "/shop/skincare-serums",
            "/shop/skincare-sunscreen",
            "/shop/skincare-eye-creams",
            "/shop/skincare-masks"
        ]
        
        for category in categories:
            if len(products) >= max_products:
                break
                
            try:
                logger.info(f"Scraping Sephora category: {category}")
                category_url = base_url + category
                
                if self.use_selenium and self.driver:
                    self.driver.get(category_url)
                    time.sleep(random.uniform(3, 5))
                    
                    # Scroll to load more products
                    self._scroll_page()
                    
                    # Get product links
                    product_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/product/']")
                    product_links = [elem.get_attribute('href') for elem in product_elements]
                else:
                    response = self.session.get(category_url)
                    if response.status_code != 200:
                        continue
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    product_elements = soup.find_all('a', href=re.compile(r'/product/'))
                    product_links = [urljoin(base_url, elem['href']) for elem in product_elements]
                
                for link in product_links[:8]:
                    if len(products) >= max_products:
                        break
                        
                    product_data = self._scrape_sephora_product_enhanced(link)
                    if product_data:
                        products.append(product_data)
                        time.sleep(random.uniform(2, 4))
                        
            except Exception as e:
                logger.error(f"Error scraping Sephora category {category}: {e}")
                
        return products
    
    def _scrape_sephora_product_enhanced(self, url: str) -> Optional[Dict]:
        """Enhanced scraping of individual product from Sephora"""
        try:
            if self.use_selenium and self.driver:
                self.driver.get(url)
                time.sleep(random.uniform(2, 4))
                
                # Wait for product info to load
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-at='product_name']"))
                    )
                except:
                    pass
                
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
            else:
                response = self.session.get(url)
                if response.status_code != 200:
                    return None
                soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product name
            name_elem = soup.find('span', {'data-at': 'product_name'}) or soup.find('h1')
            if not name_elem:
                return None
            name = name_elem.get_text(strip=True)
            
            # Extract brand
            brand_elem = soup.find('span', {'data-at': 'brand_name'}) or soup.find('a', href=re.compile(r'/brand/'))
            brand = brand_elem.get_text(strip=True) if brand_elem else "Unknown"
            
            # Extract price
            price = 0
            price_elem = soup.find('span', {'data-at': 'price'})
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'\$?(\d+(?:\.\d{2})?)', price_text)
                if price_match:
                    price = int(float(price_match.group(1)) * 100)
            
            # Extract ingredients from product description
            ingredients_list = ""
            description_elem = soup.find('div', {'data-at': 'product_description'}) or soup.find('div', class_='description')
            if description_elem:
                description_text = description_elem.get_text()
                # Look for ingredients in description
                ingredients_match = re.search(r'Ingredients[:\s]*(.*?)(?:\n|$)', description_text, re.IGNORECASE)
                if ingredients_match:
                    ingredients_list = ingredients_match.group(1).strip()
            
            # Extract star ingredients
            star_ingredients = ""
            if ingredients_list:
                all_ingredients = [ing.strip() for ing in ingredients_list.split(',')]
                star_ingredients = ", ".join(all_ingredients[:5])
            
            product_type = self._determine_product_type_enhanced(name, ingredients_list)
            
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
    
    def _scroll_page(self):
        """Scroll page to load more content"""
        if not self.driver:
            return
            
        try:
            # Scroll down gradually
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
        except Exception as e:
            logger.warning(f"Error scrolling page: {e}")
    
    def _determine_product_type_enhanced(self, name: str, ingredients: str = "") -> str:
        """Enhanced product type determination"""
        name_lower = name.lower()
        ingredients_lower = ingredients.lower()
        
        type_keywords = {
            'Cleanser': ['cleanser', 'wash', 'foam', 'gel cleanser', 'cleansing', 'face wash'],
            'Toner': ['toner', 'toning', 'astringent'],
            'Serum': ['serum', 'booster', 'concentrate'],
            'Moisturizer': ['moisturizer', 'cream', 'lotion', 'hydrating', 'emollient'],
            'Sunscreen': ['sunscreen', 'spf', 'sun protection', 'uv protection'],
            'Mask': ['mask', 'sheet mask', 'clay mask', 'peel-off'],
            'Treatment': ['treatment', 'spot treatment', 'acne', 'retinol', 'peptide'],
            'Eye Cream': ['eye', 'eye cream', 'eye gel', 'eye serum'],
            'Essence': ['essence'],
            'Ampoule': ['ampoule', 'ampule'],
            'Lip Care': ['lip', 'lip balm', 'lip treatment', 'lip mask'],
            'Body Care': ['body', 'body lotion', 'body cream', 'body wash']
        }
        
        # Check name first
        for product_type, keywords in type_keywords.items():
            if any(keyword in name_lower for keyword in keywords):
                return product_type
        
        # Check ingredients if name didn't match
        if ingredients:
            for product_type, keywords in type_keywords.items():
                if any(keyword in ingredients_lower for keyword in keywords):
                    return product_type
        
        return 'Other'
    
    def _generate_realistic_price(self, brand: str, product_type: str) -> int:
        """Generate realistic price based on brand and product type"""
        brand_lower = brand.lower()
        
        # Brand price tiers (in cents)
        luxury_brands = ['skinceuticals', 'estee lauder', 'lancome', 'clinique']
        mid_brands = ['paulas choice', 'cerave', 'la roche posay', 'neutrogena']
        budget_brands = ['the ordinary', 'cetaphil', 'aveeno', 'eucerin']
        
        if any(brand in brand_lower for brand in luxury_brands):
            base_price = random.randint(3000, 8000)  # $30-80
        elif any(brand in brand_lower for brand in mid_brands):
            base_price = random.randint(1500, 4000)  # $15-40
        elif any(brand in brand_lower for brand in budget_brands):
            base_price = random.randint(800, 2500)   # $8-25
        else:
            base_price = random.randint(1000, 3500)  # $10-35
        
        # Adjust based on product type
        type_multipliers = {
            'Serum': 1.3,
            'Treatment': 1.4,
            'Sunscreen': 1.1,
            'Eye Cream': 1.2,
            'Mask': 0.8,
            'Cleanser': 0.9,
            'Toner': 0.9,
            'Moisturizer': 1.0
        }
        
        multiplier = type_multipliers.get(product_type, 1.0)
        return int(base_price * multiplier)
    
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
    
    def run_scraper(self, sources: List[str] = None, method: str = 'api', max_products: int = 100) -> None:
        """Run the scraper with specified sources and method"""
        if sources is None:
            sources = ['incidecoder']
        
        all_products = []
        
        for source in sources:
            logger.info(f"Starting to scrape from {source}")
            
            if source == 'incidecoder':
                products = self.scrape_incidecoder_enhanced(max_products // len(sources))
            elif source == 'sephora':
                products = self.scrape_sephora_enhanced(max_products // len(sources))
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
    parser = argparse.ArgumentParser(description='Enhanced Skincare Product Scraper')
    parser.add_argument('--sources', nargs='+', 
                       choices=['incidecoder', 'sephora'],
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
    parser.add_argument('--max-products', type=int, default=100,
                       help='Maximum number of products to scrape')
    parser.add_argument('--no-selenium', action='store_true',
                       help='Disable Selenium and use requests only')
    
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
    scraper = EnhancedSkincareScraper(
        api_base_url=args.api_url,
        db_config=db_config,
        use_selenium=not args.no_selenium
    )
    
    try:
        # Run scraper
        scraper.run_scraper(
            sources=args.sources, 
            method=args.method,
            max_products=args.max_products
        )
    finally:
        # Cleanup
        if scraper.driver:
            scraper.driver.quit()

if __name__ == "__main__":
    main()
