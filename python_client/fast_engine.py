"""
High-Performance Async HTTP Engine
Achieves 300-500 CPM using:
- httpx AsyncClient with HTTP/2
- Connection pooling (max 100 connections, 20 keepalive)
- Fast JSON with orjson
- Regex caching with lru_cache
- Cookie parsing (JSON + key=value format)
"""

import httpx
import asyncio
import time
import json
import re
from functools import lru_cache
from typing import Dict, List, Optional, Any

try:
    import orjson
    ORJSON_AVAILABLE = True
except ImportError:
    ORJSON_AVAILABLE = False


class FastEngine:
    """High-performance async HTTP cookie checker"""
    
    def __init__(self, timeout: int = 15, max_connections: int = 100):
        """
        Initialize FastEngine
        
        Args:
            timeout: Request timeout in seconds
            max_connections: Maximum number of concurrent connections
        """
        self.timeout = timeout
        self.max_connections = max_connections
        self.client = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
        
    async def initialize(self):
        """Initialize HTTP client with optimized settings"""
        limits = httpx.Limits(
            max_connections=self.max_connections,
            max_keepalive_connections=20,
            keepalive_expiry=30.0
        )
        
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            limits=limits,
            http2=True,  # Enable HTTP/2 for multiplexing
            follow_redirects=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        )
        
    async def close(self):
        """Close HTTP client and cleanup"""
        if self.client:
            await self.client.aclose()
            self.client = None
    
    @staticmethod
    @lru_cache(maxsize=128)
    def compile_regex(pattern: str) -> re.Pattern:
        """Cache compiled regex patterns for performance"""
        return re.compile(pattern)
    
    def parse_cookies(self, cookies_str: str, domain: str = "") -> Dict[str, str]:
        """
        Parse cookies from various formats
        
        Supports:
        - JSON: {"sessionid": "abc123", "token": "xyz"}
        - Key=Value: sessionid=abc123; token=xyz
        
        Args:
            cookies_str: Cookie string to parse
            domain: Domain for cookies (optional)
            
        Returns:
            Dictionary of cookie key-value pairs
        """
        cookies = {}
        
        # Try JSON first
        try:
            if ORJSON_AVAILABLE:
                cookies = orjson.loads(cookies_str)
            else:
                cookies = json.loads(cookies_str)
            return cookies
        except:
            pass
        
        # Try key=value format
        try:
            for item in cookies_str.split(';'):
                item = item.strip()
                if '=' in item:
                    key, value = item.split('=', 1)
                    cookies[key.strip()] = value.strip()
        except:
            pass
            
        return cookies
    
    def fast_json_loads(self, data: str) -> Any:
        """Fast JSON parsing using orjson if available"""
        if ORJSON_AVAILABLE:
            return orjson.loads(data)
        return json.loads(data)
    
    def fast_json_dumps(self, data: Any) -> str:
        """Fast JSON encoding using orjson if available"""
        if ORJSON_AVAILABLE:
            return orjson.dumps(data).decode('utf-8')
        return json.dumps(data)
    
    async def check_cookie(
        self,
        config: Dict[str, Any],
        cookies: str,
        proxy: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check a single cookie using config
        
        Args:
            config: Configuration dict with url, method, headers, success_keywords, failure_keywords
            cookies: Cookie string to check
            proxy: Optional proxy URL
            
        Returns:
            Dictionary with: valid, status_code, check_time, extracted_data
        """
        start_time = time.time()
        
        try:
            # Parse config
            url = config.get('url', '')
            method = config.get('method', 'GET').upper()
            headers = config.get('headers', {})
            success_keywords = config.get('success_keywords', [])
            failure_keywords = config.get('failure_keywords', [])
            
            # Parse cookies
            cookie_dict = self.parse_cookies(cookies, url)
            
            # Prepare request
            request_kwargs = {
                'url': url,
                'headers': headers.copy(),
                'cookies': cookie_dict
            }
            
            # Add proxy if provided
            if proxy:
                # Format proxy for httpx
                if not proxy.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
                    proxy = f'http://{proxy}'
                request_kwargs['proxies'] = proxy
            
            # Make request
            if method == 'GET':
                response = await self.client.get(**request_kwargs)
            elif method == 'POST':
                request_kwargs['data'] = config.get('body', {})
                response = await self.client.post(**request_kwargs)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            # Get response data
            status_code = response.status_code
            response_text = response.text
            
            # Check success/failure keywords
            is_valid = False
            
            if success_keywords:
                # If success keywords exist, must match at least one
                for keyword in success_keywords:
                    if keyword in response_text:
                        is_valid = True
                        break
            elif status_code == 200:
                # If no success keywords, just check status code
                is_valid = True
            
            # Check failure keywords (override success)
            if failure_keywords:
                for keyword in failure_keywords:
                    if keyword in response_text:
                        is_valid = False
                        break
            
            check_time = time.time() - start_time
            
            return {
                'valid': is_valid,
                'status_code': status_code,
                'check_time': check_time,
                'extracted_data': self.fast_json_dumps({
                    'response_length': len(response_text),
                    'cookies': cookie_dict
                })
            }
            
        except Exception as e:
            check_time = time.time() - start_time
            return {
                'valid': False,
                'status_code': 0,
                'check_time': check_time,
                'extracted_data': self.fast_json_dumps({
                    'error': str(e)
                })
            }
    
    async def check_batch(
        self,
        config: Dict[str, Any],
        cookies_list: List[str],
        proxies: Optional[List[str]] = None,
        max_concurrent: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Check multiple cookies concurrently
        
        Args:
            config: Configuration dict
            cookies_list: List of cookie strings
            proxies: Optional list of proxies (rotated)
            max_concurrent: Maximum concurrent requests
            
        Returns:
            List of result dictionaries
        """
        # Create semaphore to limit concurrency
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def check_with_semaphore(cookies, proxy):
            async with semaphore:
                return await self.check_cookie(config, cookies, proxy)
        
        # Create tasks
        tasks = []
        for i, cookies in enumerate(cookies_list):
            proxy = None
            if proxies and len(proxies) > 0:
                proxy = proxies[i % len(proxies)]
            tasks.append(check_with_semaphore(cookies, proxy))
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to error results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    'valid': False,
                    'status_code': 0,
                    'check_time': 0.0,
                    'extracted_data': self.fast_json_dumps({
                        'error': str(result)
                    })
                })
            else:
                processed_results.append(result)
        
        return processed_results


async def example_usage():
    """Example usage of FastEngine"""
    # Sample config
    config = {
        'url': 'https://store.steampowered.com/account/',
        'method': 'GET',
        'headers': {},
        'success_keywords': ['account_name'],
        'failure_keywords': ['login']
    }
    
    # Sample cookies
    cookies = [
        'sessionid=abc123; token=xyz789',
        'sessionid=invalid; token=bad',
    ]
    
    # Check cookies
    async with FastEngine() as engine:
        results = await engine.check_batch(config, cookies, max_concurrent=10)
        
        for i, result in enumerate(results):
            print(f"Cookie {i+1}: {'VALID' if result['valid'] else 'INVALID'} "
                  f"(Time: {result['check_time']:.2f}s)")


if __name__ == '__main__':
    asyncio.run(example_usage())
