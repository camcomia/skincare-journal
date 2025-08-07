# Test Suite Documentation

This directory contains comprehensive tests for the Skincare Log application.

## 📁 Directory Structure

```
tests/
├── config.py                    # Test configuration and utilities
├── README.md                   # This file
├── run_all_tests.py           # Main test runner
├── integration/
│   └── test_api_integration.py # Comprehensive API integration tests
├── debug/
│   └── test_oil_free_debug.py # Specialized debug tests for oil-free issues
└── unit/                      # Unit tests (future)
```

## 🚀 Quick Start

### Run All Tests
```bash
python tests/run_all_tests.py
```

### Run Individual Test Suites
```bash
# Integration tests
python tests/integration/test_api_integration.py

# Oil-free debug tests
python tests/debug/test_oil_free_debug.py

# Quick smoke test
python tests/run_all_tests.py
```

## 📋 Test Categories

### 1. Integration Tests (`integration/`)
Comprehensive tests that verify the entire API functionality:

- **Basic API Connectivity**: Verifies the API is accessible
- **Search Functionality**: Tests search across product names, brands, and ingredients
- **Brand Filtering**: Validates brand-specific filtering
- **Tag Filtering**: Tests all tag filters (Alcohol-Free, Fragrance-Free, Oil-Free, Sensitive Skin Friendly)
- **Sorting Functionality**: Verifies all sorting options (name, price, brand, etc.)
- **Combined Filters**: Tests complex filter combinations
- **Pagination**: Validates pagination functionality
- **Performance**: Measures response times
- **Data Validation**: Ensures returned data has correct structure

### 2. Debug Tests (`debug/`)
Specialized tests for debugging specific issues:

- **Oil-Free Tag Debug**: Detailed analysis of oil detection logic
- **Edge Case Testing**: Tests boundary conditions
- **Product Analysis**: Analyzes all products for oil detection
- **API vs Logic Validation**: Compares API results with expected logic

### 3. Smoke Tests
Quick tests to verify basic functionality before running full suites.

## 🔧 Configuration

The test configuration is centralized in `config.py`:

- **BASE_URL**: API endpoint (default: `http://localhost:8080/api/products`)
- **TIMEOUT**: Request timeout (default: 10 seconds)
- **MAX_RETRIES**: Retry attempts for failed requests (default: 3)

## 📊 Test Results

Tests provide detailed logging with:
- ✅ Success indicators
- ❌ Failure indicators
- ⚠️ Warning indicators
- 📊 Performance metrics
- 📈 Success rates

## 🐛 Debugging

### Oil-Free Tag Issues
If you're debugging oil-free tag problems:

1. Run the debug tests: `python tests/debug/test_oil_free_debug.py`
2. Check the detailed analysis output
3. Verify the oil detection logic matches backend implementation

### API Issues
If you're debugging API problems:

1. Run the smoke test first: `python tests/run_all_tests.py`
2. Check connectivity to `http://localhost:8080`
3. Verify backend is running and accessible

## 📝 Adding New Tests

### Adding Integration Tests
1. Add new test methods to `APIIntegrationTests` class
2. Follow the naming convention: `test_<feature_name>`
3. Use `self.logger.log_success()` and `self.logger.log_failure()`

### Adding Debug Tests
1. Create new test class in `debug/` directory
2. Inherit from base test structure
3. Focus on specific debugging scenarios

### Example Test Method
```python
def test_new_feature(self):
    """Test description"""
    try:
        response = TestConfig.make_request("", {"param": "value"})
        
        if TestConfig.check_response(response, "Test name"):
            data = response.json()
            # Your validation logic here
            self.logger.log_success("Test name", "Success details")
        else:
            self.logger.log_failure("Test name", "Failure details")
            
    except Exception as e:
        self.logger.log_failure("Test name", f"Exception: {e}")
```

## 🎯 Test Coverage

The test suite covers:

- ✅ **API Endpoints**: All GET endpoints
- ✅ **Search Functionality**: Text search across multiple fields
- ✅ **Filtering**: Brand, tag, and type filters
- ✅ **Sorting**: All sort options
- ✅ **Pagination**: Page-based results
- ✅ **Performance**: Response time monitoring
- ✅ **Data Validation**: Structure verification
- ✅ **Error Handling**: Exception scenarios
- ✅ **Edge Cases**: Boundary conditions

## 🔍 Troubleshooting

### Common Issues

1. **Connection Refused**: Backend not running
   - Start the Spring Boot backend
   - Verify it's running on `http://localhost:8080`

2. **Timeout Errors**: Slow responses
   - Check backend performance
   - Increase timeout in `config.py` if needed

3. **Oil-Free Filter Issues**: 
   - Run debug tests to analyze
   - Check backend oil detection logic
   - Verify product data integrity

### Test Output Interpretation

- **✅ Success**: Test passed as expected
- **❌ Failure**: Test failed - check logs for details
- **⚠️ Warning**: Test passed but with concerns
- **📊 Performance**: Response time metrics
- **📈 Summary**: Overall test results

## 🚀 Continuous Integration

The test suite is designed to be run in CI/CD pipelines:

```bash
# Run all tests and exit with code 0 if all pass
python tests/run_all_tests.py
```

The test runner will exit with appropriate exit codes for CI integration.
