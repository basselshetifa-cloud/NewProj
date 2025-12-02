"""
Multi-Process Performance Checker
Achieves 1000-1500 CPM using:
- multiprocessing.Pool (all CPU cores)
- Async FastEngine in each process
- Efficient work distribution
- Result aggregation
"""

import asyncio
import multiprocessing as mp
from typing import Dict, List, Optional, Any
import time
from fast_engine import FastEngine


class PerformanceChecker:
    """Multi-process cookie checker using all CPU cores"""
    
    def __init__(self, threads_per_process: int = 50):
        """
        Initialize PerformanceChecker
        
        Args:
            threads_per_process: Number of concurrent async tasks per process
        """
        self.threads_per_process = threads_per_process
        self.num_processes = mp.cpu_count()
    
    @staticmethod
    def _process_chunk(args: tuple) -> List[Dict[str, Any]]:
        """
        Process a chunk of cookies in a separate process
        
        This is a static method so it can be pickled for multiprocessing
        
        Args:
            args: Tuple of (config, cookies_chunk, proxies, threads_per_process)
            
        Returns:
            List of result dictionaries
        """
        config, cookies_chunk, proxies, threads_per_process = args
        
        # Run async processing in this process
        return asyncio.run(
            PerformanceChecker._async_process(
                config, cookies_chunk, proxies, threads_per_process
            )
        )
    
    @staticmethod
    async def _async_process(
        config: Dict[str, Any],
        cookies_chunk: List[str],
        proxies: Optional[List[str]],
        threads_per_process: int
    ) -> List[Dict[str, Any]]:
        """
        Async processing of cookie chunk
        
        Args:
            config: Configuration dict
            cookies_chunk: List of cookies to process
            proxies: Optional list of proxies
            threads_per_process: Concurrency limit
            
        Returns:
            List of result dictionaries
        """
        async with FastEngine() as engine:
            results = await engine.check_batch(
                config,
                cookies_chunk,
                proxies,
                max_concurrent=threads_per_process
            )
        return results
    
    def check_cookies(
        self,
        config: Dict[str, Any],
        cookies_list: List[str],
        proxies: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Check cookies using multi-processing for maximum speed
        
        Args:
            config: Configuration dict
            cookies_list: List of cookie strings
            proxies: Optional list of proxies
            
        Returns:
            List of result dictionaries
        """
        if len(cookies_list) == 0:
            return []
        
        # Split cookies into chunks (one per CPU core, up to num_processes)
        num_chunks = min(self.num_processes, len(cookies_list))
        chunk_size = max(1, len(cookies_list) // num_chunks)
        chunks = [
            cookies_list[i:i + chunk_size]
            for i in range(0, len(cookies_list), chunk_size)
        ]
        
        # Prepare arguments for each process
        process_args = [
            (config, chunk, proxies, self.threads_per_process)
            for chunk in chunks
        ]
        
        # Process chunks in parallel
        with mp.Pool(processes=min(self.num_processes, len(chunks))) as pool:
            chunk_results = pool.map(self._process_chunk, process_args)
        
        # Flatten results
        all_results = []
        for chunk_result in chunk_results:
            all_results.extend(chunk_result)
        
        return all_results
    
    def check_single(
        self,
        config: Dict[str, Any],
        cookie: str,
        proxy: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check a single cookie (for GUI compatibility)
        
        Args:
            config: Configuration dict
            cookie: Cookie string
            proxy: Optional proxy
            
        Returns:
            Result dictionary
        """
        # Use async directly for single cookie
        result = asyncio.run(self._check_single_async(config, cookie, proxy))
        return result
    
    @staticmethod
    async def _check_single_async(
        config: Dict[str, Any],
        cookie: str,
        proxy: Optional[str]
    ) -> Dict[str, Any]:
        """Async single cookie check"""
        async with FastEngine() as engine:
            result = await engine.check_cookie(config, cookie, proxy)
        return result


def example_usage():
    """Example usage of PerformanceChecker"""
    import json
    
    # Sample config
    config = {
        'url': 'https://store.steampowered.com/account/',
        'method': 'GET',
        'headers': {},
        'success_keywords': ['account_name'],
        'failure_keywords': ['login']
    }
    
    # Generate test cookies
    cookies = [f'sessionid=test{i}; token=token{i}' for i in range(100)]
    
    # Check cookies
    start_time = time.time()
    checker = PerformanceChecker(threads_per_process=50)
    results = checker.check_cookies(config, cookies)
    elapsed = time.time() - start_time
    
    # Calculate stats
    valid_count = sum(1 for r in results if r['valid'])
    cpm = int((len(cookies) / elapsed) * 60)
    
    print(f"\n{'='*60}")
    print(f"Performance Test Results")
    print(f"{'='*60}")
    print(f"Total Cookies: {len(cookies)}")
    print(f"Valid: {valid_count}")
    print(f"Invalid: {len(cookies) - valid_count}")
    print(f"Time: {elapsed:.2f}s")
    print(f"CPM: {cpm}")
    print(f"CPU Cores Used: {mp.cpu_count()}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    # Required for Windows multiprocessing
    mp.freeze_support()
    example_usage()
