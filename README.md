# Cookie Checker - Professional Suite

Multi-engine cookie validation tool with 3 interface options.

## 🎨 GUI Options

### 1. Original GUI (Simple & Fast)
**File:** `cookie_checker.py`

Simple keyword-based checker with clean interface:
- 22+ service support (Steam, Discord, Netflix, etc.)
- Multi-threaded scanning (50 threads)
- Real-time CPM tracking
- Search and filter results

**Run:**
```bash
cd python_client
python cookie_checker.py
```

**Build:**
```bash
build_original.bat
→ dist\CookieChecker-Original.exe
```

### 2. Advanced GUI (Config-Based)
**File:** `gui.py`

Multi-engine system with config designer:
- Go engine (fast)
- Playwright (stealth)
- Selenium (automation)
- Visual config editor

**Run:**
```bash
python gui.py
```

### 3. Standalone Fast (Performance)
**File:** `standalone_gui.py`

High-performance engines:
- Fast Python (300-500 CPM)
- Multi-Process (1000-1500 CPM)
- Selenium headless

**Run:**
```bash
python standalone_gui.py
```

**Build:**
```bash
build_fast.bat
→ dist\CookieChecker-Fast.exe
```

## 📦 Installation

```bash
# Original GUI (minimal)
pip install customtkinter

# Advanced GUI (full)
pip install -r requirements.txt

# Fast engines
pip install -r requirements_fast.txt
```

## 🚀 Quick Start

**Simplest option (Original GUI):**
```bash
cd python_client
python cookie_checker.py
```

1. Click "LOAD COOKIES" - select folder with cookie files
2. (Optional) Click "LOAD PROXY" - load proxy list
3. Select services to check
4. Click "START"

**Results saved to:** `CookieChecker_Results/[service]_hits.txt`

## 📊 Performance Comparison

| GUI | Speed | Memory | Best For |
|-----|-------|--------|----------|
| Original | ~100 CPM | 50MB | Quick scans, keyword checking |
| Advanced | Varies | 200MB+ | Config-based, multi-engine |
| Standalone Fast | 1000+ CPM | 150MB | Large batches, speed |

## 🛠️ Features

### Original GUI
- ✅ 22+ service keyword detection
- ✅ Multi-threaded (50 threads)
- ✅ Proxy support
- ✅ Real-time CPM
- ✅ Search/filter output
- ✅ Auto-save hits

### Advanced GUI
- ✅ Config designer (LoliScript)
- ✅ 3 engines (Go/Playwright/Selenium)
- ✅ Advanced parsing (LR, CSS, XPath, Regex)
- ✅ 30+ functions (Hash, HMAC, Base64, etc.)
- ✅ Browser automation

### Standalone Fast
- ✅ Async HTTP/2 engine
- ✅ Multi-process (all CPU cores)
- ✅ 300-1500 CPM
- ✅ Connection pooling
- ✅ No external servers needed

## 📝 Config Examples

See `configs/` folder for examples:
- `steam.json` - Basic Steam config
- `advanced_steam.json` - Advanced parsing
- `cloudflare_bypass.json` - Selenium automation
- `captcha_solver.json` - CAPTCHA integration

## 🤝 Contributing

PRs welcome! Please ensure:
- Code follows existing style
- No breaking changes to existing GUIs
- Update README if adding features

## 📄 License

MIT License - See LICENSE file

---

**Choose the GUI that fits your needs!** 🔥
