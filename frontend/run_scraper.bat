@echo off
echo ========================================
echo Skincare Product Scraper
echo ========================================

echo.
echo Choose scraping option:
echo 1. Basic scraper (requests only)
echo 2. Enhanced scraper (with Selenium)
echo 3. Custom configuration
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Running basic scraper...
    python skincare_scraper.py --sources incidecoder --method api --max-products 50
) else if "%choice%"=="2" (
    echo.
    echo Running enhanced scraper...
    python enhanced_scraper.py --sources incidecoder --method api --max-products 50
) else if "%choice%"=="3" (
    echo.
    echo Custom configuration:
    echo.
    set /p sources="Sources (incidecoder, sephora): "
    set /p method="Method (api, database): "
    set /p max_products="Max products: "
    set /p use_selenium="Use Selenium? (y/n): "
    
    if "%use_selenium%"=="y" (
        python enhanced_scraper.py --sources %sources% --method %method% --max-products %max_products%
    ) else (
        python enhanced_scraper.py --sources %sources% --method %method% --max-products %max_products% --no-selenium
    )
) else (
    echo Invalid choice!
    goto :eof
)

echo.
echo Scraping completed!
pause
