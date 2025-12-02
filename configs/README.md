# 📋 Config Files Documentation

This directory contains configuration files for the Hybrid Cookie Checker. Each config defines how to check cookies for a specific service.

## 📦 Config Structure

```json
{
  "name": "Service Name",
  "author": "Your Name",
  "version": "1.0",
  "url": "https://target-site.com/check",
  "method": "GET",
  "cookie_format": "netscape",
  "needs_stealth": false,
  "use_selenium": false,
  "browser_mode": "headless",
  "timeout": 15,
  "blocks": [...]
}
```

## 🧩 Block Types

### 🟢 REQUEST Block
Makes HTTP requests to APIs or web pages.

```json
{
  "type": "REQUEST",
  "url": "https://api.example.com/user",
  "method": "GET",
  "headers": {
    "Authorization": "Bearer <token>",
    "Cookie": "<COOKIES_RAW>",
    "User-Agent": "Mozilla/5.0..."
  },
  "body": "",
  "save_response": "api_response"
}
```

**Variables:**
- `<COOKIES_RAW>` - Raw cookie string
- `<COOKIE:name>` - Specific cookie value
- `<variable>` - Custom variables from previous blocks

### 🟡 PARSE Block (Enhanced)
Extract data from responses using multiple methods.

#### Left-Right (LR) Parsing
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

#### CSS Selector
```json
{
  "type": "PARSE",
  "source": "response",
  "parse_type": "CSS",
  "selector": ".user-name",
  "capture_name": "username"
}
```

#### XPath
```json
{
  "type": "PARSE",
  "source": "response",
  "parse_type": "XPath",
  "selector": "//div[@class='user-name']/text()",
  "capture_name": "username"
}
```

#### JSON Path
```json
{
  "type": "PARSE",
  "source": "response",
  "parse_type": "JSON",
  "json_path": "$.data.user.name",
  "capture_name": "username"
}
```

#### Regex
```json
{
  "type": "PARSE",
  "source": "response",
  "parse_type": "Regex",
  "pattern": "user_id\":(\\d+)",
  "capture_name": "user_id"
}
```

### 🔵 KEYCHECK Block (Enhanced)
Validate captured data with advanced comparers.

```json
{
  "type": "KEYCHECK",
  "conditions": [
    {
      "left": "<username>",
      "comparer": "Exists",
      "right": ""
    },
    {
      "left": "<email>",
      "comparer": "Contains",
      "right": "@"
    }
  ],
  "logic": "AND",
  "success": "HIT",
  "failure": "BAD"
}
```

**Comparers:**
- `EqualTo` - Exact match
- `NotEqualTo` - Not equal
- `Contains` - Contains substring
- `NotContains` - Doesn't contain
- `StartsWith` - Starts with
- `EndsWith` - Ends with
- `GreaterThan` - Numeric comparison
- `LessThan` - Numeric comparison
- `MatchesRegex` - Regex pattern match
- `Exists` - Variable exists and not empty
- `DoesNotExist` - Variable doesn't exist or empty

**Logic:**
- `AND` - All conditions must pass
- `OR` - At least one condition must pass

**Outcomes:**
- `HIT` - Valid cookie
- `BAD` - Invalid cookie
- `RETRY` - Retry check
- `BAN` - IP banned
- `CUSTOM` - Custom status

### 🟣 FUNCTION Block
Apply functions to data.

```json
{
  "type": "FUNCTION",
  "function": "Hash-SHA256",
  "input": "<password>",
  "save_as": "hashed_password"
}
```

**Available Functions:**

#### Hashing
- `Hash-MD5` - MD5 hash
- `Hash-SHA1` - SHA1 hash
- `Hash-SHA256` - SHA256 hash
- `Hash-SHA384` - SHA384 hash
- `Hash-SHA512` - SHA512 hash
- `HMAC` - HMAC with key (param1: key)

#### Encoding
- `Base64-Encode` - Encode to Base64
- `Base64-Decode` - Decode from Base64
- `URLEncode` - URL encode
- `URLDecode` - URL decode
- `HTMLEntityEncode` - HTML entity encode
- `HTMLEntityDecode` - HTML entity decode

#### String Manipulation
- `Replace` - Replace text (param1: find, param2: replace)
- `Substring` - Extract substring (param1: start, param2: length)
- `CharAt` - Get character at index (param1: index)
- `CountOccurrences` - Count occurrences (param1: substring)
- `Length` - Get string length
- `Uppercase` - Convert to uppercase
- `Lowercase` - Convert to lowercase
- `Reverse` - Reverse string
- `Trim` - Remove whitespace
- `Split` - Split to list (param1: delimiter)
- `Join` - Join list (param1: delimiter)

#### Random
- `RandomNum` - Random number (param1: min, param2: max)
- `RandomString` - Random string (param1: length)

#### Time/Date
- `UnixTimeToDate` - Convert Unix timestamp to date
- `DateToUnixTime` - Convert date to Unix timestamp
- `CurrentUnixTime` - Get current Unix time

### 🟠 UTILITY Block
Various utility operations.

```json
{
  "type": "UTILITY",
  "utility": "Delay",
  "input": "1000",
  "save_as": "result"
}
```

**Available Utilities:**

#### List Operations
- `List-Create` - Create list
- `List-Length` - Get list length
- `List-Join` - Join list elements
- `List-Sort` - Sort list
- `List-Add` - Add element
- `List-Remove` - Remove element
- `List-RemoveDuplicates` - Remove duplicates
- `List-Random` - Get random element
- `List-Shuffle` - Shuffle list

#### Variable Operations
- `Variable-Set` - Set variable value
- `Variable-Split` - Split string to list

#### File Operations
- `File-Exists` - Check if file exists
- `File-Read` - Read file content
- `File-Write` - Write to file
- `File-Append` - Append to file
- `File-Delete` - Delete file

#### Folder Operations
- `Folder-Exists` - Check if folder exists
- `Folder-Create` - Create folder
- `Folder-Delete` - Delete folder

#### Other
- `Delay` - Sleep for milliseconds

### 🟤 CAPTCHA Block
Solve CAPTCHAs using external services.

```json
{
  "type": "CAPTCHA",
  "service": "2Captcha",
  "api_key": "YOUR_API_KEY",
  "site_key": "6Le-wvkSAAAAA...",
  "page_url": "https://example.com/login",
  "captcha_type": "reCAPTCHA v2",
  "save_as": "captcha_token"
}
```

**Services:**
- `2Captcha`
- `AntiCaptcha`
- `DeathByCaptcha`
- `ImageTyperz`

**Types:**
- `reCAPTCHA v2`
- `reCAPTCHA v3`
- `hCaptcha`

### 🔴 TCP Block
Raw TCP socket communication.

```json
{
  "type": "TCP",
  "host": "example.com",
  "port": "443",
  "send_data": "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n",
  "timeout": "10",
  "ssl": true,
  "save_as": "tcp_response"
}
```

### 🔴 BYPASS_CF Block
Bypass Cloudflare protection.

```json
{
  "type": "BYPASS_CF",
  "url": "https://protected-site.com",
  "user_agent": "Mozilla/5.0...",
  "timeout": "30",
  "save_cookies": true
}
```

### 🟢 BROWSER_ACTION Block
Perform actions in browser (Selenium/Playwright).

```json
{
  "type": "BROWSER_ACTION",
  "action": "Click",
  "selector": "#login-button",
  "by": "CSS",
  "value": "",
  "timeout": "10"
}
```

**Actions:**
- `Click` - Click element
- `Type` - Type text (value: text to type)
- `Wait` - Wait for element
- `Screenshot` - Take screenshot (value: filename)
- `ExecuteJS` - Execute JavaScript (value: script)
- `Scroll` - Scroll page
- `SwitchTab` - Switch browser tab
- `SwitchIframe` - Switch to iframe
- `CloseTab` - Close tab

**By:**
- `CSS` - CSS selector
- `XPath` - XPath expression
- `ID` - Element ID
- `Class` - Class name

### 🟡 ELEMENT_ACTION Block
Interact with page elements.

```json
{
  "type": "ELEMENT_ACTION",
  "selector": "#user-email",
  "by": "CSS",
  "action": "GetText",
  "attribute": "",
  "save_as": "email"
}
```

**Actions:**
- `GetText` - Get element text
- `GetAttribute` - Get attribute (attribute: name)
- `GetHTML` - Get inner HTML
- `CheckExists` - Check if exists
- `CheckVisible` - Check if visible

### 🟣 EXECUTE_JS Block
Execute JavaScript in browser.

```json
{
  "type": "EXECUTE_JS",
  "script": "return document.title;",
  "save_as": "page_title"
}
```

### 🟢 NAVIGATE Block
Navigate browser.

```json
{
  "type": "NAVIGATE",
  "action": "NavigateTo",
  "url": "https://example.com",
  "timeout": "10"
}
```

**Actions:**
- `NavigateTo` - Go to URL
- `GoBack` - Go back
- `GoForward` - Go forward
- `Refresh` - Refresh page
- `WaitForLoad` - Wait for page load

## 📝 Example Configs

### Basic Steam Check
```json
{
  "name": "Steam Basic",
  "url": "https://store.steampowered.com/account/",
  "method": "GET",
  "cookie_format": "netscape",
  "blocks": [
    {
      "type": "REQUEST",
      "url": "https://store.steampowered.com/account/",
      "method": "GET",
      "headers": {"Cookie": "<COOKIES_RAW>"},
      "save_response": "page"
    },
    {
      "type": "KEYCHECK",
      "conditions": [{"left": "<page>", "comparer": "Contains", "right": "account_name"}],
      "success": "HIT",
      "failure": "BAD"
    }
  ]
}
```

### Advanced with Multiple Parsing
See `advanced_steam.json` for a complete example with:
- Multiple parse blocks (LR and Regex)
- Function blocks for data processing
- Advanced keycheck with multiple conditions

### Selenium with Cloudflare Bypass
See `cloudflare_bypass.json` for:
- Cloudflare bypass
- Browser navigation
- Element interaction
- Screenshots

### CAPTCHA Solving
See `captcha_solver.json` for:
- CAPTCHA service integration
- Form filling
- JavaScript execution
- Login automation

## 🎯 Best Practices

1. **Use Variables** - Capture and reuse data between blocks
2. **Minimize Requests** - Combine data extraction in single requests
3. **Error Handling** - Use KEYCHECK for validation
4. **Stealth Mode** - Enable for sites with bot detection
5. **Selenium** - Use only when needed (slower than HTTP)
6. **Timeouts** - Set appropriate timeouts for each service
7. **Testing** - Test configs with small batches first

## 🔧 Engines

Configs can run on three engines:

1. **Go Engine** (Fast)
   - REQUEST, PARSE (JSON/Regex), KEYCHECK
   - Best for simple HTTP checks

2. **Playwright Engine** (Stealth)
   - All blocks except Selenium-specific
   - Anti-detection features
   - Good for protected sites

3. **Selenium Engine** (Maximum Control)
   - All blocks including CAPTCHA, BROWSER_ACTION
   - Full browser automation
   - Undetected ChromeDriver support

Choose the right engine based on your needs:
- Simple API checks → Go
- Protected sites → Playwright
- Complex automation → Selenium

## 📚 More Examples

Check the `configs/` directory for more examples:
- `steam.json` - Basic Steam check
- `discord.json` - Discord check
- `github.json` - GitHub check
- `advanced_steam.json` - Advanced parsing
- `cloudflare_bypass.json` - CF bypass
- `captcha_solver.json` - CAPTCHA solving
