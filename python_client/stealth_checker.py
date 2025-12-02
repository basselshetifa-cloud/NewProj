from playwright.sync_api import sync_playwright
try:
    from playwright_stealth import stealth_sync
except ImportError:
    stealth_sync = None
import json
import time

class StealthChecker:
    def __init__(self):
        self.playwright = None
        self.browser = None
    
    def check(self, service, file_path, cookies, proxy):
        if not self.playwright:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
        
        try:
            with open(f'../configs/{service.lower()}.json', 'r') as f:
                config = json.load(f)
        except Exception as e:
            return type('Response', (), {
                'valid': False,
                'status_code': 0,
                'check_time': 0,
                'extracted_data': json.dumps({'error': str(e)})
            })
        
        context_options = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        if proxy:
            context_options['proxy'] = {'server': proxy}
        
        context = self.browser.new_context(**context_options)
        
        cookies_list = self.parse_cookies(cookies, config['url'])
        if cookies_list:
            context.add_cookies(cookies_list)
        
        page = context.new_page()
        
        if stealth_sync:
            stealth_sync(page)
        
        start_time = time.time()
        
        try:
            response = page.goto(config['url'], wait_until='networkidle', timeout=15000)
            content = page.content()
            
            valid = response.status == config.get('blocks', [{}])[0].get('success_code', 200)
            for keyword in config.get('success_keywords', []):
                if keyword.lower() in content.lower():
                    valid = True
                    break
            
            extracted_data = self.extract_data(page, config)
            
            check_time = time.time() - start_time
            
            return type('Response', (), {
                'valid': valid,
                'status_code': response.status,
                'check_time': check_time,
                'extracted_data': json.dumps(extracted_data)
            })
        
        except Exception as e:
            return type('Response', (), {
                'valid': False,
                'status_code': 0,
                'check_time': time.time() - start_time,
                'extracted_data': json.dumps({'error': str(e)})
            })
        
        finally:
            context.close()
    
    def parse_cookies(self, cookie_string, domain):
        cookies = []
        
        try:
            cookie_dict = json.loads(cookie_string)
            for name, value in cookie_dict.items():
                cookies.append({
                    'name': name,
                    'value': str(value),
                    'domain': domain.split('/')[2],
                    'path': '/'
                })
        except:
            for line in cookie_string.split(';'):
                if '=' in line:
                    name, value = line.split('=', 1)
                    cookies.append({
                        'name': name.strip(),
                        'value': value.strip(),
                        'domain': domain.split('/')[2] if '/' in domain else domain,
                        'path': '/'
                    })
        
        return cookies
    
    def extract_data(self, page, config):
        data = {}
        
        if 'blocks' in config:
            for block in config['blocks']:
                if block.get('type') == 'PARSE' and 'captures' in block:
                    for key, selector in block['captures'].items():
                        try:
                            if selector.startswith('$.'):
                                continue
                            element = page.query_selector(selector)
                            if element:
                                data[key] = element.inner_text()
                        except:
                            pass
        
        return data
    
    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()