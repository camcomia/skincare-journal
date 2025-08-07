#!/usr/bin/env python3
"""
Test runner for all test suites
"""

import sys
import os
import time
from datetime import datetime

# Add the tests directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import test_api_connection

def run_test_suite(test_name: str, test_function):
    """Run a test suite and return results"""
    print(f"\n{'='*60}")
    print(f"🧪 Running {test_name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        test_function()
        success = True
        error = None
    except Exception as e:
        success = False
        error = str(e)
    
    end_time = time.time()
    duration = end_time - start_time
    
    return {
        'name': test_name,
        'success': success,
        'error': error,
        'duration': duration
    }

def main():
    """Run all test suites"""
    print("🚀 Starting Comprehensive Test Suite")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test suites to run
    test_suites = [
        ("API Connection Test", test_api_connection),
    ]
    
    # Import test modules
    try:
        from integration.test_filter_functionality import run_all_filter_tests
        test_suites.append(("Filter Functionality Tests", run_all_filter_tests))
    except ImportError as e:
        print(f"⚠️  Could not import filter functionality tests: {e}")
    
    try:
        from debug.test_oil_free_debug import debug_oil_free_detection, test_oil_free_api_endpoint
        def run_oil_free_tests():
            debug_oil_free_detection()
            test_oil_free_api_endpoint()
        test_suites.append(("Oil-Free Debug Tests", run_oil_free_tests))
    except ImportError as e:
        print(f"⚠️  Could not import oil-free debug tests: {e}")
    
    # Run all test suites
    results = []
    total_start_time = time.time()
    
    for test_name, test_function in test_suites:
        result = run_test_suite(test_name, test_function)
        results.append(result)
    
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    failed = 0
    
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        duration = f"{result['duration']:.2f}s"
        
        print(f"{status} {result['name']} ({duration})")
        
        if result['error']:
            print(f"   Error: {result['error']}")
        
        if result['success']:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Overall Results:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📊 Total: {len(results)}")
    print(f"   ⏱️  Total Time: {total_duration:.2f}s")
    
    if failed == 0:
        print(f"\n🎉 All test suites passed!")
    else:
        print(f"\n⚠️  {failed} test suite(s) failed")
    
    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
