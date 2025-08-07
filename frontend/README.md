# Skincare Product Web Scraper

A comprehensive web scraper for collecting skincare product data from multiple sources and injecting it into your database via API or direct database connection.

## Features

- **Multiple Sources**: Scrapes from INCIDecoder, Sephora, and other skincare websites
- **Dual Methods**: Add products via API or direct database insertion
- **Enhanced Scraping**: Uses Selenium for better JavaScript-heavy site scraping
- **Rate Limiting**: Respectful scraping with configurable delays
- **Comprehensive Data**: Extracts product name, brand, ingredients, star ingredients, product type, and price
- **Logging**: Detailed logging for monitoring and debugging
- **Flexible Configuration**: Command-line arguments for customization

## Prerequisites

- Python 3.7 or higher
- Chrome browser (for Selenium-based scraping)
- MySQL database (optional, for direct database insertion)
- Your skincare API running on localhost:8080

## Installation

1. **Clone or download the scraper files to your project directory**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **For enhanced scraping (Selenium), install Chrome browser if not already installed**

## Quick Start

### Option 1: Using PowerShell (Recommended for Windows)

```powershell
# Basic usage with default settings
.\run_scraper.ps1

# Custom configuration
.\run_scraper.ps1 -Sources "incidecoder,sephora" -MaxProducts 100 -UseSelenium
```

### Option 2: Using Batch File (Windows)

```cmd
# Run the interactive batch file
run_scraper.bat
```

### Option 3: Direct Python Execution

```bash
# Basic scraper (requests only)
python skincare_scraper.py --sources incidecoder --method api --max-products 50

# Enhanced scraper (with Selenium)
python enhanced_scraper.py --sources incidecoder --method api --max-products 50

# Multiple sources
python enhanced_scraper.py --sources incidecoder sephora --method api --max-products 100

# Direct database insertion
python enhanced_scraper.py --sources incidecoder --method database --db-user root --db-password your_password
```

## Configuration Options

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--sources` | Sources to scrape (incidecoder, sephora) | incidecoder |
| `--method` | Method to add products (api, database) | api |
| `--api-url` | API base URL | http://localhost:8080/api |
| `--max-products` | Maximum number of products to scrape | 100 |
| `--db-host` | Database host | localhost |
| `--db-port` | Database port | 3306 |
| `--db-name` | Database name | skincare_db |
| `--db-user` | Database user | root |
| `--db-password` | Database password | (empty) |
| `--no-selenium` | Disable Selenium and use requests only | False |

### Database Configuration

If using direct database insertion, ensure your MySQL database has a `products` table with the following structure:

```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(255) NOT NULL,
    ingredients_list TEXT,
    star_ingredients TEXT,
    product_type VARCHAR(100),
    price INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Integration

The scraper is designed to work with your existing skincare API. It expects the API to:

- Accept POST requests to `/api/products`
- Accept JSON data with fields: `name`, `brand`, `ingredientsList`, `starIngredients`, `productType`, `price`
- Return 200 or 201 status code for successful creation

### Example API Request

```json
{
    "name": "Hyaluronic Acid 2% + B5",
    "brand": "The Ordinary",
    "ingredientsList": "Aqua (Water), Sodium Hyaluronate, Panthenol, Glycerin, Sodium PCA, Sodium Lactate, Arginine, PCA, Sodium Chloride, Sodium Hyaluronate Crosspolymer, Xanthan Gum, Trisodium Ethylenediamine Disuccinate, Citric Acid, Isoceteth-20, Ethoxydiglycol, Phenoxyethanol, Chlorphenesin",
    "starIngredients": "Sodium Hyaluronate, Panthenol, Glycerin",
    "productType": "Serum",
    "price": 680
}
```

## Data Sources

### INCIDecoder
- **URL**: https://incidecoder.com
- **Features**: Comprehensive ingredient lists, detailed product information
- **Brands**: The Ordinary, CeraVe, La Roche-Posay, Paula's Choice, etc.

### Sephora
- **URL**: https://www.sephora.com
- **Features**: Wide product selection, pricing information
- **Categories**: Cleansers, moisturizers, serums, sunscreens, etc.

## Product Type Detection

The scraper automatically categorizes products based on keywords in the product name and ingredients:

- **Cleanser**: wash, foam, gel cleanser, cleansing
- **Toner**: toner, toning, astringent
- **Serum**: serum, booster, concentrate
- **Moisturizer**: moisturizer, cream, lotion, hydrating
- **Sunscreen**: sunscreen, spf, sun protection
- **Mask**: mask, sheet mask, clay mask
- **Treatment**: treatment, spot treatment, acne
- **Eye Cream**: eye, eye cream, eye gel
- **Essence**: essence
- **Ampoule**: ampoule, ampule
- **Lip Care**: lip, lip balm, lip treatment
- **Body Care**: body, body lotion, body cream

## Price Generation

The scraper generates realistic prices based on:
- **Brand tier**: Luxury, mid-range, or budget brands
- **Product type**: Serums and treatments typically cost more
- **Market positioning**: Based on actual retail prices

## Logging

The scraper provides detailed logging:
- **File**: `scraper.log` or `enhanced_scraper.log`
- **Console**: Real-time progress updates
- **Levels**: INFO, WARNING, ERROR

## Error Handling

The scraper includes robust error handling:
- Network timeouts and retries
- Invalid HTML parsing
- Database connection errors
- API endpoint failures
- Rate limiting and respectful scraping

## Best Practices

1. **Start Small**: Begin with 10-20 products to test your setup
2. **Monitor Logs**: Check log files for any issues
3. **Respect Rate Limits**: The scraper includes delays to be respectful to websites
4. **Backup Data**: Always backup your database before large imports
5. **Test API**: Ensure your API is running and accessible before scraping

## Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   - Ensure Chrome browser is installed
   - The scraper will automatically download the appropriate ChromeDriver

2. **Database Connection Issues**
   - Verify MySQL is running
   - Check database credentials
   - Ensure the products table exists

3. **API Connection Issues**
   - Verify your API is running on localhost:8080
   - Check API endpoint `/api/products` is accessible
   - Test with a simple POST request

4. **Selenium Issues**
   - Use `--no-selenium` flag to disable Selenium
   - Install Chrome browser if not present
   - Check ChromeDriver compatibility

### Performance Tips

- Use Selenium for JavaScript-heavy sites (Sephora)
- Use requests-only mode for faster scraping of simple sites
- Adjust `--max-products` based on your needs
- Consider running during off-peak hours

## Legal and Ethical Considerations

- **Respect robots.txt**: The scraper respects website terms
- **Rate limiting**: Built-in delays prevent overwhelming servers
- **Educational use**: Intended for personal/educational purposes
- **Terms of service**: Always check website terms before scraping

## Support

For issues or questions:
1. Check the log files for detailed error messages
2. Verify your API and database connections
3. Test with smaller product counts first
4. Ensure all dependencies are properly installed

## License

This scraper is provided for educational and personal use. Please respect website terms of service and use responsibly.
