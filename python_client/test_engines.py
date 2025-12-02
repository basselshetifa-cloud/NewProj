#!/usr/bin/env python3
"""
Test script for high-performance engines
Tests FastEngine and PerformanceChecker functionality
"""

import asyncio
import time
import sys


def test_fast_engine():
    """Test FastEngine basic functionality"""
    print("\n" + "="*60)
    print("Testing FastEngine")
    print("="*60)
    
    try:
        from fast_engine import FastEngine
        
        # Test config (using httpbin for testing)
        config = {
            'url': 'https://httpbin.org/cookies',
            'method': 'GET',
            'headers': {},
            'success_keywords': [],
            'failure_keywords': []
        }
        
        # Test cookies
        test_cookies = [
            'test_cookie=abc123; session=xyz789',
            'another_test=value123',
        ]
        
        async def run_tests():
            async with FastEngine(timeout=10, max_connections=10) as engine:
                # Test 1: Single cookie check
                print("\n[Test 1/4] Single cookie check...")
                result = await engine.check_cookie(config, test_cookies[0])
                assert 'valid' in result
                assert 'check_time' in result
                assert 'status_code' in result
                print(f"  ✓ Result: status={result['status_code']}, time={result['check_time']:.2f}s")
                
                # Test 2: Batch check
                print("\n[Test 2/4] Batch check (2 cookies)...")
                results = await engine.check_batch(config, test_cookies, max_concurrent=2)
                assert len(results) == len(test_cookies)
                print(f"  ✓ Checked {len(results)} cookies")
                
                # Test 3: JSON cookie parsing
                print("\n[Test 3/4] JSON cookie parsing...")
                json_cookie = '{"sessionid": "abc123", "token": "xyz789"}'
                parsed = engine.parse_cookies(json_cookie)
                assert len(parsed) == 2
                assert 'sessionid' in parsed
                assert 'token' in parsed
                print(f"  ✓ Parsed {len(parsed)} cookies from JSON")
                
                # Test 4: Key=Value cookie parsing
                print("\n[Test 4/4] Key=Value cookie parsing...")
                kv_cookie = 'sessionid=abc123; token=xyz789; user=test'
                parsed = engine.parse_cookies(kv_cookie)
                assert len(parsed) == 3
                print(f"  ✓ Parsed {len(parsed)} cookies from key=value")
            
            return True
        
        success = asyncio.run(run_tests())
        
        if success:
            print("\n✅ FastEngine: ALL TESTS PASSED")
            return True
        
    except Exception as e:
        print(f"\n❌ FastEngine: TEST FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_performance_checker():
    """Test PerformanceChecker basic functionality"""
    print("\n" + "="*60)
    print("Testing PerformanceChecker")
    print("="*60)
    
    try:
        from performance_checker import PerformanceChecker
        import multiprocessing as mp
        
        # Test config
        config = {
            'url': 'https://httpbin.org/cookies',
            'method': 'GET',
            'headers': {},
            'success_keywords': [],
            'failure_keywords': []
        }
        
        # Generate test cookies
        num_cookies = 20
        test_cookies = [f'test{i}=value{i}' for i in range(num_cookies)]
        
        print(f"\n[Test 1/3] Detected CPU cores: {mp.cpu_count()}")
        
        # Test 2: Multi-process check
        print(f"\n[Test 2/3] Multi-process check ({num_cookies} cookies)...")
        start_time = time.time()
        checker = PerformanceChecker(threads_per_process=10)
        results = checker.check_cookies(config, test_cookies)
        elapsed = time.time() - start_time
        
        assert len(results) == num_cookies, f"Expected {num_cookies} results, got {len(results)}"
        cpm = int((num_cookies / elapsed) * 60) if elapsed > 0 else 0
        print(f"  ✓ Processed {len(results)} cookies in {elapsed:.2f}s ({cpm} CPM)")
        
        # Test 3: Single cookie check
        print("\n[Test 3/3] Single cookie check...")
        result = checker.check_single(config, test_cookies[0])
        assert 'valid' in result
        assert 'check_time' in result
        print(f"  ✓ Single check completed in {result['check_time']:.2f}s")
        
        print("\n✅ PerformanceChecker: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ PerformanceChecker: TEST FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("High-Performance Engine Test Suite")
    print("="*60)
    print("\nNote: These tests require internet connection (httpbin.org)")
    
    results = {}
    
    # Test FastEngine
    results['FastEngine'] = test_fast_engine()
    
    # Test PerformanceChecker
    results['PerformanceChecker'] = test_performance_checker()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {name:25} {status}")
    
    all_passed = all(results.values())
    print("\n" + "="*60)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("="*60 + "\n")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED")
        print("="*60 + "\n")
        return 1


if __name__ == '__main__':
    import multiprocessing as mp
    mp.freeze_support()  # Required for Windows multiprocessing
    sys.exit(main())
