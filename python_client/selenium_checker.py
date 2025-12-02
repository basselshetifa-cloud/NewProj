from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import json
import time
import os
from datetime import datetime

try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False

try:
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


class SeleniumChecker:
    """
    Selenium-based cookie checker with advanced features:
    - Chrome WebDriver support (user provides chromedriver)
    - Undetected ChromeDriver integration (stealth mode)
    - Cookie injection support (all formats)
    - Screenshot capture on success
    - Headless/headed mode toggle
    - Proxy support (HTTP/SOCKS)
    - Custom User-Agent
    - Anti-detection features (remove webdriver flags)
    - Wait for page load
    - Error handling with fallback
    """
    
    def __init__(self, use_undetected=True, headless=True, chromedriver_path=None):
        """
        Initialize SeleniumChecker
        
        Args:
            use_undetected (bool): Use undetected_chromedriver for stealth
            headless (bool): Run browser in headless mode
            chromedriver_path (str): Path to chromedriver executable (optional)
        """
        self.driver = None
        self.use_undetected = use_undetected and UNDETECTED_AVAILABLE
        self.headless = headless
        self.chromedriver_path = chromedriver_path
        self.screenshots_dir = "screenshots"
        
        # Create screenshots directory if it doesn't exist
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)
    
    def setup_driver(self, proxy=None, user_agent=None):
        """
        Setup Chrome driver with options
        
        Args:
            proxy (str): Proxy URL (format: host:port or protocol://host:port)
            user_agent (str): Custom user agent string
        
        Returns:
            WebDriver instance
        """
        if self.use_undetected:
            # Use undetected_chromedriver for maximum stealth
            options = uc.ChromeOptions()
            
            if self.headless:
                options.add_argument('--headless=new')
            
            # Additional stealth arguments
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            
            if user_agent:
                options.add_argument(f'--user-agent={user_agent}')
            
            if proxy:
                # Parse proxy format
                if not proxy.startswith('http'):
                    proxy = f'http://{proxy}'
                options.add_argument(f'--proxy-server={proxy}')
            
            try:
                self.driver = uc.Chrome(options=options, driver_executable_path=self.chromedriver_path)
            except Exception as e:
                print(f"Undetected ChromeDriver failed: {e}, falling back to standard driver")
                return self._setup_standard_driver(proxy, user_agent)
        else:
            return self._setup_standard_driver(proxy, user_agent)
        
        return self.driver
    
    def _setup_standard_driver(self, proxy=None, user_agent=None):
        """Setup standard Chrome WebDriver"""
        options = Options()
        
        if self.headless:
            options.add_argument('--headless=new')
        
        # Anti-detection arguments
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        
        # Set user agent
        if not user_agent:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        options.add_argument(f'--user-agent={user_agent}')
        
        # Set proxy
        if proxy:
            if not proxy.startswith('http'):
                proxy = f'http://{proxy}'
            options.add_argument(f'--proxy-server={proxy}')
        
        # Try to use webdriver-manager if available
        try:
            if self.chromedriver_path:
                service = Service(self.chromedriver_path)
            elif WEBDRIVER_MANAGER_AVAILABLE:
                service = Service(ChromeDriverManager().install())
            else:
                service = Service()  # Will use PATH
            
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"Standard ChromeDriver setup failed: {e}")
            raise
        
        # Additional anti-detection via CDP
        try:
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": user_agent
            })
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except:
            pass
        
        return self.driver
    
    def check(self, service, file_path, cookies, proxy=None, user_agent=None):
        """
        Main checking function
        
        Args:
            service (str): Service name (e.g., "Steam", "Discord")
            file_path (str): Path to cookie file (unused, kept for compatibility)
            cookies (str): Cookie content (JSON, Netscape, or header format)
            proxy (str): Proxy URL (optional)
            user_agent (str): Custom user agent (optional)
        
        Returns:
            Response object with validation results
        """
        start_time = time.time()
        
        try:
            # Load service config
            config_path = f'../configs/{service.lower()}.json'
            if not os.path.exists(config_path):
                config_path = f'configs/{service.lower()}.json'
            
            with open(config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            return self._create_response(False, 0, time.time() - start_time, {'error': f'Config load error: {str(e)}'})
        
        # Setup driver if not already done
        if not self.driver:
            try:
                self.setup_driver(proxy, user_agent)
            except Exception as e:
                return self._create_response(False, 0, time.time() - start_time, {'error': f'Driver setup error: {str(e)}'})
        
        try:
            # Parse and inject cookies
            url = config.get('url', '')
            domain = self._extract_domain(url)
            
            # Navigate to domain first to set cookies
            self.driver.get(url)
            time.sleep(1)  # Brief wait for page to initialize
            
            # Inject cookies
            cookies_list = self._parse_cookies(cookies, domain)
            if cookies_list:
                for cookie in cookies_list:
                    try:
                        self.driver.add_cookie(cookie)
                    except Exception as e:
                        print(f"Cookie injection warning: {e}")
            
            # Refresh page with cookies
            self.driver.refresh()
            
            # Wait for page load
            self.wait_for_page_load(timeout=config.get('timeout', 15))
            
            # Get page content
            page_source = self.driver.page_source
            current_url = self.driver.current_url
            
            # Validate based on config
            valid = self._validate_response(page_source, current_url, config)
            
            # Extract data if valid
            extracted_data = {}
            if valid:
                extracted_data = self._extract_data(config)
                
                # Take screenshot on success
                if PILLOW_AVAILABLE:
                    screenshot_path = self.take_screenshot(f"{service}_{int(time.time())}")
                    if screenshot_path:
                        extracted_data['screenshot'] = screenshot_path
            
            check_time = time.time() - start_time
            
            return self._create_response(valid, 200, check_time, extracted_data)
        
        except TimeoutException:
            return self._create_response(False, 0, time.time() - start_time, {'error': 'Page load timeout'})
        except WebDriverException as e:
            return self._create_response(False, 0, time.time() - start_time, {'error': f'WebDriver error: {str(e)}'})
        except Exception as e:
            return self._create_response(False, 0, time.time() - start_time, {'error': f'Check error: {str(e)}'})
    
    def inject_cookies(self, cookies, domain):
        """
        Inject cookies into browser
        
        Args:
            cookies (list): List of cookie dictionaries
            domain (str): Domain for cookies
        """
        for cookie in cookies:
            try:
                cookie_dict = {
                    'name': cookie.get('name', ''),
                    'value': cookie.get('value', ''),
                    'domain': cookie.get('domain', domain),
                    'path': cookie.get('path', '/'),
                }
                
                # Add optional fields if present
                if 'expiry' in cookie:
                    cookie_dict['expiry'] = cookie['expiry']
                if 'secure' in cookie:
                    cookie_dict['secure'] = cookie['secure']
                if 'httpOnly' in cookie:
                    cookie_dict['httpOnly'] = cookie['httpOnly']
                
                self.driver.add_cookie(cookie_dict)
            except Exception as e:
                print(f"Failed to inject cookie {cookie.get('name', 'unknown')}: {e}")
    
    def wait_for_element(self, selector, by=By.CSS_SELECTOR, timeout=10):
        """
        Wait for element to be present
        
        Args:
            selector (str): Element selector
            by (By): Selenium By type (CSS_SELECTOR, XPATH, ID, etc.)
            timeout (int): Maximum wait time in seconds
        
        Returns:
            WebElement or None
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            return element
        except TimeoutException:
            return None
    
    def wait_for_page_load(self, timeout=10):
        """Wait for page to fully load"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
        except TimeoutException:
            pass
    
    def take_screenshot(self, filename):
        """
        Capture screenshot
        
        Args:
            filename (str): Screenshot filename (without extension)
        
        Returns:
            str: Path to screenshot file or None
        """
        if not self.driver or not PILLOW_AVAILABLE:
            return None
        
        try:
            screenshot_path = os.path.join(self.screenshots_dir, f"{filename}.png")
            self.driver.save_screenshot(screenshot_path)
            return screenshot_path
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return None
    
    def execute_javascript(self, script):
        """
        Execute JavaScript in browser context
        
        Args:
            script (str): JavaScript code to execute
        
        Returns:
            Result of script execution
        """
        if not self.driver:
            return None
        
        try:
            return self.driver.execute_script(script)
        except Exception as e:
            print(f"JavaScript execution failed: {e}")
            return None
    
    def close(self):
        """Close driver and cleanup"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def _extract_domain(self, url):
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return url.split('/')[2] if '/' in url else url
    
    def _parse_cookies(self, cookie_string, domain):
        """
        Parse cookies from various formats
        
        Args:
            cookie_string (str): Cookie content
            domain (str): Target domain
        
        Returns:
            list: List of cookie dictionaries
        """
        cookies = []
        
        try:
            # Try JSON format first
            cookie_dict = json.loads(cookie_string)
            for name, value in cookie_dict.items():
                cookies.append({
                    'name': name,
                    'value': str(value),
                    'domain': domain,
                    'path': '/'
                })
            return cookies
        except:
            pass
        
        # Try Netscape format
        if '\t' in cookie_string:
            lines = cookie_string.split('\n')
            for line in lines:
                if line.startswith('#') or not line.strip():
                    continue
                parts = line.split('\t')
                if len(parts) >= 7:
                    cookies.append({
                        'name': parts[5],
                        'value': parts[6],
                        'domain': parts[0],
                        'path': parts[2],
                        'secure': parts[3] == 'TRUE',
                        'expiry': int(parts[4]) if parts[4].isdigit() else None
                    })
            return cookies
        
        # Try header format
        for pair in cookie_string.split(';'):
            if '=' in pair:
                name, value = pair.split('=', 1)
                cookies.append({
                    'name': name.strip(),
                    'value': value.strip(),
                    'domain': domain,
                    'path': '/'
                })
        
        return cookies
    
    def _validate_response(self, page_source, current_url, config):
        """
        Validate response based on config criteria
        
        Args:
            page_source (str): HTML page source
            current_url (str): Current URL
            config (dict): Service configuration
        
        Returns:
            bool: True if valid, False otherwise
        """
        # Check success keywords
        success_keywords = config.get('success_keywords', [])
        if success_keywords:
            for keyword in success_keywords:
                if keyword.lower() in page_source.lower():
                    return True
        
        # Check failure keywords
        failure_keywords = config.get('failure_keywords', [])
        if failure_keywords:
            for keyword in failure_keywords:
                if keyword.lower() in page_source.lower():
                    return False
        
        # Check if redirected to login
        if 'login' in current_url.lower() or 'signin' in current_url.lower():
            return False
        
        # Default to False if no success indicator
        return len(success_keywords) == 0 and len(failure_keywords) > 0
    
    def _extract_data(self, config):
        """
        Extract data from page based on config
        
        Args:
            config (dict): Service configuration
        
        Returns:
            dict: Extracted data
        """
        data = {}
        
        if 'blocks' not in config:
            return data
        
        for block in config['blocks']:
            if block.get('type') == 'PARSE' and 'captures' in block:
                for key, selector in block['captures'].items():
                    try:
                        if selector.startswith('$.'):
                            # JSONPath - skip for now
                            continue
                        
                        # Try CSS selector
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if element:
                            data[key] = element.text
                    except:
                        try:
                            # Try XPath
                            element = self.driver.find_element(By.XPATH, selector)
                            if element:
                                data[key] = element.text
                        except:
                            pass
        
        return data
    
    def _create_response(self, valid, status_code, check_time, extracted_data):
        """Create response object"""
        return type('Response', (), {
            'valid': valid,
            'status_code': status_code,
            'check_time': check_time,
            'extracted_data': json.dumps(extracted_data)
        })
