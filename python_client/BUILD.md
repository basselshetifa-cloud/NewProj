# 🔧 Building Standalone Executables

This document explains how to build standalone executables for the Cookie Checker application.

## 🐛 PyInstaller + Playwright-Stealth Fix

### The Problem

When building with PyInstaller, the application crashes with:
```
FileNotFoundError: [Errno 2] No such file or directory: 
'C:\\Users\\...\\AppData\\Local\\Temp\\_MEI149362\\playwright_stealth\\js\\generate.magic.arrays.js'
```

**Root Cause:** PyInstaller doesn't automatically include `playwright-stealth` JavaScript files in the EXE bundle.

### The Solution

Our build scripts now:
1. **Detect playwright-stealth** installation automatically
2. **Include JS files** using `--add-data` and `--collect-all` flags
3. **Graceful fallback** - build without Playwright if not installed
4. **Optional imports** - all engines work independently

---

## 📦 Build Options

### Option 1: Full Build (Recommended)
**Includes all engines: Fast + Multi-Process + Playwright + Selenium**

#### Windows
```bash
cd python_client
build_fast.bat
```

#### Linux/Mac
```bash
cd python_client
chmod +x build_fast.sh
./build_fast.sh
```

**Output:** `dist/CookieChecker-Fast.exe` (Windows) or `dist/CookieChecker-Fast` (Linux/Mac)

**Features:**
- ✅ All 4 engines included
- ✅ Playwright-stealth JS files included
- ✅ ~40-60MB file size
- ✅ No external dependencies needed

---

### Option 2: Minimal Build (No Playwright)
**Includes: Fast + Multi-Process + Selenium only**

#### Windows
```bash
cd python_client
build_minimal.bat
```

**Output:** `dist/CookieChecker-Minimal.exe`

**Features:**
- ✅ Fast + Multi-Process + Selenium
- ❌ No Playwright (avoids JS file issues)
- ✅ ~25-35MB file size (smaller)
- ✅ No Playwright dependencies

**Use when:**
- You don't need Playwright stealth mode
- Want smaller file size
- Avoid playwright-stealth dependency issues

---

## 🔍 Build Process Details

### Full Build Script Logic

1. **Validation** - Check required files exist
2. **Install Dependencies** - Install from `requirements_fast.txt`
3. **Detect Playwright-Stealth**:
   ```python
   import playwright_stealth, os
   print(os.path.dirname(playwright_stealth.__file__))
   ```
4. **Build with PyInstaller**:
   - **If Playwright found:** Include with `--add-data` and `--collect-all`
   - **If Playwright missing:** Build without it
5. **Cleanup** - Remove build artifacts
6. **Verify** - Check executable exists

### PyInstaller Flags Explained

#### For Playwright-Stealth:
```bash
--add-data "%STEALTH_PATH%;playwright_stealth"  # Include JS files
--hidden-import=playwright                       # Import playwright
--hidden-import=playwright_stealth               # Import stealth
--collect-all playwright_stealth                 # Collect all stealth files
--collect-all playwright                         # Collect all playwright files
```

#### For Other Engines:
```bash
--hidden-import=httpx                           # Fast engine HTTP client
--hidden-import=orjson                          # Fast JSON parser
--hidden-import=h2                              # HTTP/2 support
--hidden-import=selenium                        # Selenium engine
--hidden-import=undetected_chromedriver         # Anti-detection
--collect-all customtkinter                     # GUI framework
```

---

## 🧪 Testing Your Build

### 1. Build the Executable
```bash
build_fast.bat    # or build_fast.sh on Linux/Mac
```

### 2. Run the Executable
```bash
cd dist
CookieChecker-Fast.exe    # Windows
./CookieChecker-Fast      # Linux/Mac
```

### 3. Verify Engines
The GUI should show:
- ✅ 🚀 Multi-Process (~1000 CPM)
- ✅ ⚡ Fast Python (~300 CPM)
- ✅ 🕵️ Playwright (~80 CPM) - if playwright-stealth installed
- ✅ 🌐 Selenium (~50 CPM) - if selenium installed

### 4. Test Cookie Checking
1. Select a test cookie file
2. Choose an engine
3. Click "▶️ START CHECKING"
4. Verify results appear in tabs

---

## 🚨 Troubleshooting

### Build Fails: "playwright_stealth not found"
**Solution:** The script will build without Playwright automatically. This is expected if you don't have it installed.

### Build Fails: "configs directory not found"
**Solution:** Ensure you're in the `python_client` directory and `configs` exists in parent directory.

### Runtime Error: "FileNotFoundError" for JS files
**Solution:** 
1. Use the full build script (not manual PyInstaller)
2. Or use the minimal build (no Playwright)

### EXE is too large
**Solution:** Use `build_minimal.bat` to exclude Playwright (~15-20MB smaller)

### Missing Engine in GUI
**Expected behavior:** Only installed engines appear. The app gracefully handles missing dependencies.

---

## 📊 Build Comparison

| Build Type | Size | Engines | Playwright | Best For |
|-----------|------|---------|------------|----------|
| **Full** | 40-60MB | All 4 | ✅ Yes | Maximum features |
| **Minimal** | 25-35MB | 3 (no Playwright) | ❌ No | Smaller size, no stealth |

---

## 🔧 Advanced: Manual Build

If you need to customize the build:

```bash
# Install dependencies
pip install -r requirements_fast.txt
pip install pyinstaller

# Find playwright-stealth path
python -c "import playwright_stealth, os; print(os.path.dirname(playwright_stealth.__file__))"

# Build with custom flags
pyinstaller --onefile --windowed \
    --name "CookieChecker-Custom" \
    --add-data "configs:configs" \
    --add-data "<STEALTH_PATH>:playwright_stealth" \
    --hidden-import=httpx \
    --hidden-import=playwright \
    --hidden-import=playwright_stealth \
    --collect-all playwright_stealth \
    --collect-all playwright \
    --optimize=2 \
    standalone_gui.py
```

---

## 🎯 Which Build Should I Use?

### Use Full Build (`build_fast.bat`) if:
- ✅ You want all engine options
- ✅ You need Playwright stealth mode
- ✅ You have playwright-stealth installed
- ✅ File size doesn't matter

### Use Minimal Build (`build_minimal.bat`) if:
- ✅ You don't need Playwright
- ✅ You want smaller file size
- ✅ You want to avoid playwright-stealth issues
- ✅ Fast + Multi-Process + Selenium is enough

---

## 📝 Build Output

Successful build shows:
```
========================================
Build complete!
========================================
Executable: dist\CookieChecker-Fast.exe

  ✓ Playwright-stealth included (Full build)
  ✓ All engines available
  ✓ Expected Performance: 500-1500 CPM
```

Or for minimal build:
```
========================================
Minimal Build Complete!
========================================
Executable: dist\CookieChecker-Minimal.exe

Includes: Fast Python + Multi-Process + Selenium
Does NOT include: Playwright (avoids JS file issues)
```

---

## 💡 Tips

1. **First Time:** Use full build to get all features
2. **Having Issues:** Try minimal build
3. **Distribution:** Test EXE on clean Windows VM
4. **Development:** Use `python standalone_gui.py` directly (no build needed)

---

## 🔗 Related Files

- `build_fast.bat` / `build_fast.sh` - Full build with Playwright
- `build_minimal.bat` - Minimal build without Playwright
- `standalone_gui.py` - Full version (4 engines)
- `standalone_gui_minimal.py` - Minimal version (3 engines)
- `stealth_checker.py` - Playwright stealth engine (optional)
- `requirements_fast.txt` - Dependencies

---

## ✅ Success Criteria

After building, verify:
- [ ] EXE starts without errors
- [ ] GUI shows available engines
- [ ] Fast/Multi-Process engines work
- [ ] Selenium works (if installed)
- [ ] Playwright works (if included in full build)
- [ ] No FileNotFoundError for JS files

---

**Questions?** Check the issue: https://github.com/basselshetifa-cloud/NewProj/issues/...
