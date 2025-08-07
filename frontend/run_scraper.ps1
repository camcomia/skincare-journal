# Skincare Product Scraper PowerShell Script
param(
    [string]$Sources = "incidecoder",
    [string]$Method = "api",
    [int]$MaxProducts = 50,
    [switch]$UseSelenium,
    [string]$ApiUrl = "http://localhost:8080/api"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Skincare Product Scraper" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found! Please install Python first." -ForegroundColor Red
    exit 1
}

# Check if required packages are installed
Write-Host "`nChecking required packages..." -ForegroundColor Yellow
$requiredPackages = @("requests", "beautifulsoup4", "mysql-connector-python", "lxml")

foreach ($package in $requiredPackages) {
    try {
        python -c "import $package" 2>$null
        Write-Host "✓ $package" -ForegroundColor Green
    } catch {
        Write-Host "✗ $package - Installing..." -ForegroundColor Yellow
        pip install $package
    }
}

# Install Selenium packages if needed
if ($UseSelenium) {
    Write-Host "`nInstalling Selenium packages..." -ForegroundColor Yellow
    $seleniumPackages = @("selenium", "webdriver-manager", "fake-useragent")
    
    foreach ($package in $seleniumPackages) {
        try {
            python -c "import $package" 2>$null
            Write-Host "✓ $package" -ForegroundColor Green
        } catch {
            Write-Host "✗ $package - Installing..." -ForegroundColor Yellow
            pip install $package
        }
    }
}

# Determine which script to run
if ($UseSelenium) {
    $script = "enhanced_scraper.py"
    $seleniumFlag = ""
} else {
    $script = "skincare_scraper.py"
    $seleniumFlag = "--no-selenium"
}

# Build command
$command = "python $script --sources $Sources --method $Method --max-products $MaxProducts --api-url $ApiUrl"
if ($seleniumFlag) {
    $command += " $seleniumFlag"
}

Write-Host "`nRunning command: $command" -ForegroundColor Yellow
Write-Host "Starting scraper..." -ForegroundColor Green

# Run the scraper
try {
    Invoke-Expression $command
    Write-Host "`nScraping completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "`nError running scraper: $_" -ForegroundColor Red
}

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
