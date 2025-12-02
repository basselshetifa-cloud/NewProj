# 🔥 Hybrid Cookie Checker - Advanced Edition

A high-performance cookie checker combining **Go** (speed), **Python Playwright** (stealth), and **Selenium** (browser automation) with gRPC communication and comprehensive OpenBullet-style visual config editor.

## ✨ Features

### Core Features
✅ **Triple Engine Architecture**: Go (fast) + Playwright (stealth) + Selenium (automation)  
✅ **gRPC Communication**: Lightning-fast inter-process communication  
✅ **Visual Config Editor**: Complete OpenBullet-style block-based editor with 12+ block types  
✅ **Multi-format Support**: JSON, Netscape, Header cookies  
✅ **Advanced Stealth Mode**: Playwright with anti-detection features  
✅ **Selenium Integration**: Chrome automation with undetected-chromedriver  
✅ **Multi-threading**: Check thousands of cookies concurrently  
✅ **Proxy Support**: HTTP/HTTPS/SOCKS4/SOCKS5  
✅ **Real-time Stats**: CPM, hits, errors, progress tracking  

### Advanced Features
🔥 **30+ Functions**: Hashing (MD5, SHA1-512), HMAC, Base64, URL encoding, string manipulation  
🔥 **5 Parse Types**: Left-Right (LR), CSS selectors, XPath, JSON paths, Regex  
🔥 **12 Block Types**: REQUEST, PARSE, KEYCHECK, FUNCTION, UTILITY, CAPTCHA, TCP, BYPASS_CF, BROWSER_ACTION, ELEMENT_ACTION, EXECUTE_JS, NAVIGATE  
🔥 **10+ Comparers**: EqualTo, Contains, StartsWith, GreaterThan, MatchesRegex, Exists, etc.  
🔥 **AND/OR Logic**: Complex validation with multiple conditions  
🔥 **CAPTCHA Solving**: 2Captcha, AntiCaptcha, DeathByCaptcha, ImageTyperz integration  
🔥 **Cloudflare Bypass**: Built-in CF challenge solver  
🔥 **Screenshot Capture**: Automatic screenshots on success  

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│               Python GUI (CustomTkinter)        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │   Go     │  │Playwright│  │ Selenium │     │
│  │  Engine  │  │ (Stealth)│  │ (Chrome) │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
└───────┼─────────────┼─────────────┼────────────┘
        │             │             │
        ├─ gRPC ─────┤             │
        │                           │
        ├─ Fast HTTP requests       │
        ├─ Anti-bot detection ─────┤
        └─ Full browser automation ─┘
```

**Three Engines:**
1. **Go Engine** (Fastest) - Simple HTTP checks, API requests
2. **Playwright Engine** (Stealth) - Anti-detection, JavaScript rendering
3. **Selenium Engine** (Most Powerful) - Full automation, CAPTCHA solving, CF bypass

## 📦 Installation

### Prerequisites
- **Go** 1.21+ ([Download](https://go.dev/dl/))
- **Python** 3.10+ ([Download](https://www.python.org/downloads/))
- **ChromeDriver** (for Selenium) - See [Setup Selenium](#-selenium-setup) below

### Quick Setup

1. **Clone Repository**
```bash
git clone https://github.com/basselshetifa-cloud/NewProj.git
cd NewProj
```

2. **Setup Go Engine**
```bash
cd go_engine
go mod download
protoc --go_out=. --go-grpc_out=. proto/checker.proto
go build -o checker_server
```

3. **Setup Python Client**
```bash
cd python_client
pip install -r requirements.txt
playwright install chromium
python -m grpc_tools.protoc -I../go_engine/proto --python_out=./proto --grpc_python_out=./proto ../go_engine/proto/checker.proto
```

### 🌐 Selenium Setup

For Selenium/Chrome automation support:

**Option 1: Automatic (Recommended)**
- The tool will automatically download ChromeDriver using `webdriver-manager`
- Just ensure Chrome/Chromium browser is installed

**Option 2: Manual ChromeDriver**
1. Download ChromeDriver matching your Chrome version:
   - [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
   - [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)
2. Add ChromeDriver to PATH or specify path in code

**Option 3: Undetected ChromeDriver (Best for Anti-Bot)**
- Automatically patched by `undetected-chromedriver` package
- Best for bypassing Cloudflare and bot detection
- Just check "Undetected ChromeDriver" in GUI

**Verify Installation:**
```bash
python -c "from selenium import webdriver; print('Selenium OK')"
python -c "import undetected_chromedriver; print('Undetected ChromeDriver OK')"
```

## 🚀 Usage

### 1. Start Go Server
```bash
cd go_engine
./checker_server
# Output: 🚀 Go gRPC Server running on :50051
```

### 2. Run Python GUI
```bash
cd python_client
python gui.py
```

### 3. Using the Checker

#### Basic Cookie Checking:
1. Click "Browse" to select cookie file (.txt)
2. (Optional) Select proxy file
3. Choose service from dropdown (Steam, Discord, GitHub, or custom)
4. Adjust threads (1-100)
5. **Select Engine:**
   - Default: Go Engine (fastest)
   - Check "Use Stealth Mode" for Playwright (anti-detection)
   - Check "Use Selenium" for Chrome automation
6. Click "▶️ START CHECKING"

#### Engine Selection Guide:
```
┌────────────────────┬──────────┬─────────┬──────────────┐
│ Feature            │ Go       │Playwright│ Selenium    │
├────────────────────┼──────────┼─────────┼──────────────┤
│ Speed              │ ⚡⚡⚡    │ ⚡⚡     │ ⚡           │
│ Anti-Detection     │ ❌       │ ✅✅    │ ✅✅✅      │
│ JavaScript Support │ ❌       │ ✅      │ ✅           │
│ CAPTCHA Solving    │ ❌       │ ❌      │ ✅           │
│ CF Bypass          │ ❌       │ ⚠️      │ ✅           │
│ Browser Actions    │ ❌       │ ⚠️      │ ✅           │
└────────────────────┴──────────┴─────────┴──────────────┘
```

**When to use:**
- **Go**: Simple API checks, high-speed scanning
- **Playwright**: Sites with bot detection, JavaScript required
- **Selenium**: Complex automation, CAPTCHAs, Cloudflare, browser interactions

### 4. Create Custom Configs

Click "⚙️ CONFIG EDITOR" to open the visual editor:

1. **Fill Config Info:**
   - Name, Author, Version
   - Target URL
   - HTTP method, cookie format
   - Enable Selenium/Stealth if needed

2. **Add Blocks:**
   - Select block type from dropdown
   - Click "➕ Add Block"
   - Fill in block parameters
   - Use ↑↓ buttons to reorder
   - Use 🗑️ to delete

3. **Preview & Save:**
   - Click "👁️ Preview JSON" to see config
   - Click "💾 Save Config" to export

4. **Load Existing Config:**
   - Click "📂 Load Config"
   - Select .json file from `configs/` directory

## 🧩 Block Types & Examples

### Available Block Types

The config editor supports 12 block types for maximum flexibility:

#### 1. 🟢 REQUEST Block
Make HTTP requests to APIs or websites.
```json
{
  "type": "REQUEST",
  "url": "https://api.example.com/user",
  "method": "GET",
  "headers": {
    "Cookie": "<COOKIES_RAW>",
    "Authorization": "Bearer <token>"
  },
  "save_response": "response"
}
```

#### 2. 🟡 PARSE Block (Enhanced)
Extract data using 5 methods:
- **LR (Left-Right)**: Parse between two strings
- **CSS**: CSS selectors
- **XPath**: XPath expressions  
- **JSON**: JSONPath ($.field.subfield)
- **Regex**: Regular expressions

```json
{
  "type": "PARSE",
  "source": "response",
  "parse_type": "LR",
  "left": "username\">",
  "right": "</span>",
  "capture_name": "username",
  "recursive": false,
  "case_sensitive": true
}
```

#### 3. 🔵 KEYCHECK Block (Enhanced)
Validate with 10+ comparers and AND/OR logic:
```json
{
  "type": "KEYCHECK",
  "conditions": [
    {"left": "<username>", "comparer": "Exists", "right": ""},
    {"left": "<email>", "comparer": "Contains", "right": "@"}
  ],
  "logic": "AND",
  "success": "HIT",
  "failure": "BAD"
}
```

**Comparers:** `EqualTo`, `NotEqualTo`, `Contains`, `NotContains`, `StartsWith`, `EndsWith`, `GreaterThan`, `LessThan`, `MatchesRegex`, `Exists`, `DoesNotExist`

#### 4. 🟣 FUNCTION Block
30+ functions including:
- **Hashing**: MD5, SHA1, SHA256, SHA384, SHA512, HMAC
- **Encoding**: Base64, URL, HTML entities
- **String**: Replace, Substring, Uppercase, Lowercase, Reverse, Trim, Length
- **Random**: RandomNum, RandomString
- **Time**: UnixTime conversions, CurrentUnixTime

```json
{
  "type": "FUNCTION",
  "function": "Hash-SHA256",
  "input": "<password>",
  "save_as": "hashed_password"
}
```

#### 5. 🟠 UTILITY Block
List operations, file I/O, delays:
```json
{
  "type": "UTILITY",
  "utility": "Delay",
  "input": "1000",
  "save_as": "result"
}
```

#### 6. 🟤 CAPTCHA Block (Selenium Only)
Solve CAPTCHAs with external services:
```json
{
  "type": "CAPTCHA",
  "service": "2Captcha",
  "api_key": "YOUR_KEY",
  "site_key": "6Le-wvk...",
  "page_url": "https://site.com",
  "captcha_type": "reCAPTCHA v2",
  "save_as": "captcha_token"
}
```

#### 7. 🔴 TCP Block
Raw TCP socket communication:
```json
{
  "type": "TCP",
  "host": "example.com",
  "port": "443",
  "send_data": "GET / HTTP/1.1\\r\\n",
  "ssl": true,
  "save_as": "tcp_response"
}
```

#### 8. 🔴 BYPASS_CF Block (Selenium)
Bypass Cloudflare protection:
```json
{
  "type": "BYPASS_CF",
  "url": "https://protected-site.com",
  "timeout": "30",
  "save_cookies": true
}
```

#### 9. 🟢 BROWSER_ACTION Block (Selenium)
Automate browser actions:
```json
{
  "type": "BROWSER_ACTION",
  "action": "Click",
  "selector": "#login-button",
  "by": "CSS",
  "timeout": "10"
}
```

**Actions:** `Click`, `Type`, `Wait`, `Screenshot`, `ExecuteJS`, `Scroll`, `SwitchTab`, `SwitchIframe`, `CloseTab`

#### 10. 🟡 ELEMENT_ACTION Block (Selenium)
Inspect page elements:
```json
{
  "type": "ELEMENT_ACTION",
  "selector": "#user-email",
  "by": "CSS",
  "action": "GetText",
  "save_as": "email"
}
```

#### 11. 🟣 EXECUTE_JS Block (Selenium)
Run JavaScript in browser:
```json
{
  "type": "EXECUTE_JS",
  "script": "return document.title;",
  "save_as": "page_title"
}
```

#### 12. 🟢 NAVIGATE Block (Selenium)
Control browser navigation:
```json
{
  "type": "NAVIGATE",
  "action": "NavigateTo",
  "url": "https://example.com",
  "timeout": "10"
}
```

### Example Configs

See the `configs/` directory for complete examples:
- **steam.json** - Basic Steam check
- **advanced_steam.json** - LR parsing + functions
- **cloudflare_bypass.json** - CF bypass with Selenium
- **captcha_solver.json** - Full CAPTCHA solving flow

Full documentation: [configs/README.md](configs/README.md)

## 📂 Project Structure

```
📦 NewProj/
├── 📁 go_engine/              ← Go Backend (gRPC Server)
│   ├── main.go                   • gRPC server
│   ├── config_parser.go          • Config file parser
│   ├── executor.go               • Block executor
│   ├── functions.go              • 30+ advanced functions (NEW)
│   ├── go.mod                    • Go dependencies
│   └── proto/
│       └── checker.proto         • gRPC protocol definition
├── 📁 python_client/          ← Python Frontend
│   ├── gui.py                    • Main GUI with Selenium toggle
│   ├── openbullet_editor.py      • Visual config editor (12 blocks)
│   ├── stealth_checker.py        • Playwright stealth engine
│   ├── selenium_checker.py       • Selenium Chrome engine (NEW)
│   ├── grpc_client.py            • gRPC communication
│   └── requirements.txt          • Python dependencies
├── 📁 configs/                ← Config Files
│   ├── steam.json                • Basic Steam check
│   ├── discord.json              • Discord check
│   ├── github.json               • GitHub check
│   ├── advanced_steam.json       • Advanced parsing (NEW)
│   ├── cloudflare_bypass.json    • CF bypass example (NEW)
│   ├── captcha_solver.json       • CAPTCHA solving (NEW)
│   └── README.md                 • Full block documentation
└── 📄 README.md
```

## 🎯 Tips & Best Practices

### Performance Optimization
1. **Use Go Engine** for simple HTTP checks (fastest)
2. **Use Playwright** only when needed (slower but stealthy)
3. **Use Selenium** sparingly (slowest but most powerful)
4. **Adjust Threads**: 
   - Go: 50-100 threads
   - Playwright: 10-20 threads
   - Selenium: 1-5 threads (resource intensive)

### Config Design
1. **Minimize Requests**: Combine data extraction in single requests
2. **Use Variables**: Capture once, reuse everywhere with `<variable>`
3. **Error Handling**: Always include KEYCHECK blocks
4. **Test Small**: Test configs with 10-50 cookies first
5. **Stealth Mode**: Enable for sites with Cloudflare/bot detection

### Cookie Formats
- **JSON**: `{"sessionid": "abc123", "token": "xyz"}`
- **Netscape**: Tab-separated format (from browser exports)
- **Header**: `sessionid=abc123; token=xyz`

### Proxy Setup
- Format: `protocol://host:port` or `host:port`
- Supports: HTTP, HTTPS, SOCKS4, SOCKS5
- Authentication: `http://user:pass@host:port`

## 🐛 Troubleshooting

### Go Server Won't Start
```bash
# Check if port 50051 is in use
lsof -i :50051  # Linux/Mac
netstat -ano | findstr :50051  # Windows

# Kill process and restart
kill -9 <PID>  # Linux/Mac
taskkill /F /PID <PID>  # Windows
```

### Selenium Issues
```bash
# ChromeDriver version mismatch
# Solution: Let webdriver-manager handle it automatically
pip install --upgrade webdriver-manager

# Chrome not found
# Download Chrome: https://www.google.com/chrome/

# Verify installation
python -c "from selenium import webdriver; driver = webdriver.Chrome(); driver.quit()"
```

### Playwright Issues
```bash
# Reinstall browsers
playwright install chromium --force

# Clear cache
rm -rf ~/.cache/ms-playwright  # Linux/Mac
```

### Python Package Issues
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Config Not Working
1. Check JSON syntax with [JSONLint](https://jsonlint.com/)
2. Verify variable names match: `<COOKIES_RAW>`, `<variable>`
3. Test with simple REQUEST → KEYCHECK first
4. Enable stealth/selenium if needed
5. Check logs in "All Results" tab

## 🔐 Security Notes

- **Never share configs** containing API keys or sensitive data
- **API Keys**: Store CAPTCHA API keys in environment variables
- **Proxies**: Use dedicated proxies for sensitive operations
- **Rate Limiting**: Respect target site's rate limits
- **Legal**: Only check your own cookies or with permission

## 📚 Learn More

### Documentation
- [Config Block Documentation](configs/README.md) - Complete guide to all 12 block types
- [ChromeDriver Setup](https://chromedriver.chromium.org/getting-started)
- [Undetected ChromeDriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)

### External Services
- [2Captcha](https://2captcha.com/) - CAPTCHA solving service
- [AntiCaptcha](https://anti-captcha.com/) - Alternative CAPTCHA solver

### Related Projects
- [OpenBullet](https://github.com/openbullet/openbullet) - Original inspiration
- [Playwright](https://playwright.dev/) - Browser automation
- [Selenium](https://www.selenium.dev/) - Web testing framework

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

**YashvirGaming**

## 🌟 Acknowledgments

- OpenBullet for the config format inspiration
- Playwright team for excellent browser automation
- Selenium & ChromeDriver teams
- The Go and Python communities

---

**⚠️ Disclaimer**: This tool is for educational and authorized testing purposes only. Always obtain proper authorization before checking cookies or accessing accounts that don't belong to you. The authors are not responsible for misuse of this software.

---

Made with ❤️ by YashvirGaming | [GitHub](https://github.com/basselshetifa-cloud/NewProj)

