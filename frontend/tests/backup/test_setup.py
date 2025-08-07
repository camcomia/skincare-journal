#!/usr/bin/env python3
"""
Test script to verify scraper setup and dependencies
"""

import sys
import requests
import mysql.connector
from mysql.connector import Error

def test_python_version():
    """Test Python version"""
    print("✓ Python version:", sys.version)
    if sys.version_info < (3, 7):
        print("✗ Python 3.7 or higher required")
        return False
    return True

def test_dependencies():
    """Test required dependencies"""
    dependencies = [
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4'), 
        ('mysql-connector-python', 'mysql.connector'),
        ('lxml', 'lxml')
    ]
    
    print("\nTesting dependencies:")
    all_good = True
    
    for dep_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✓ {dep_name}")
        except ImportError:
            print(f"✗ {dep_name} - Install with: pip install {dep_name}")
            all_good = False
    
    return all_good

def test_selenium_dependencies():
    """Test Selenium dependencies"""
    selenium_deps = [
        ('selenium', 'selenium'),
        ('webdriver_manager', 'webdriver_manager'),
        ('fake_useragent', 'fake_useragent')
    ]
    
    print("\nTesting Selenium dependencies:")
    all_good = True
    
    for dep_name, import_name in selenium_deps:
        try:
            __import__(import_name)
            print(f"✓ {dep_name}")
        except ImportError:
            print(f"✗ {dep_name} - Install with: pip install {dep_name}")
            all_good = False
    
    return all_good

def test_api_connection(api_url="http://localhost:8080/api"):
    """Test API connection"""
    print(f"\nTesting API connection to {api_url}:")
    
    try:
        response = requests.get(api_url.replace('/api', '/api/products'), timeout=5)
        if response.status_code in [200, 404]:  # 404 is OK if endpoint exists but no products
            print("✓ API is accessible")
            return True
        else:
            print(f"✗ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API. Make sure your backend is running on localhost:8080")
        return False
    except Exception as e:
        print(f"✗ API connection error: {e}")
        return False

def test_database_connection(host='localhost', port=3306, database='skincare_db', user='root', password='30830'):
    """Test database connection"""
    print(f"\nTesting database connection to {host}:{port}:")
    
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✓ Database connected successfully (MySQL {version[0]})")
            
            # Test if products table exists
            cursor.execute("SHOW TABLES LIKE 'skincare_products'")
            if cursor.fetchone():
                print("✓ Products table exists")
            else:
                print("⚠ Products table not found. You may need to create it.")
            
            cursor.close()
            connection.close()
            return True
        else:
            print("✗ Database connection failed")
            return False
            
    except Error as e:
        print(f"✗ Database connection error: {e}")
        return False

def test_sample_scraping():
    """Test basic scraping functionality"""
    print("\nTesting basic scraping functionality:")
    
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # Test a simple request to INCIDecoder
        response = requests.get("https://incidecoder.com", timeout=10)
        if response.status_code == 200:
            print("✓ Can access INCIDecoder")
            return True
        else:
            print(f"✗ INCIDecoder returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Scraping test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("SKINCARE SCRAPER SETUP TEST")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Selenium Dependencies", test_selenium_dependencies),
        ("API Connection", test_api_connection),
        ("Database Connection", test_database_connection),
        ("Basic Scraping", test_sample_scraping)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your scraper is ready to use.")
        print("\nNext steps:")
        print("1. Start your API server on localhost:8080")
        print("2. Run: python enhanced_scraper.py --sources incidecoder --max-products 10")
        print("3. Or use: .\\run_scraper.ps1 (Windows)")
    else:
        print("\n⚠ Some tests failed. Please fix the issues above before running the scraper.")
        
        if not any(name == "API Connection" and result for name, result in results):
            print("\n💡 Make sure your skincare API is running on localhost:8080")
        
        if not any(name == "Database Connection" and result for name, result in results):
            print("\n💡 Make sure MySQL is running and the skincare_db database exists")

if __name__ == "__main__":
    main()
