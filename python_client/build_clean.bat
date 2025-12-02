@echo off
echo 🔥 Building Cookie Checker - Clean Build
echo.

REM Install dependencies
pip install customtkinter httpx[http2] orjson h2 selenium undetected-chromedriver pyinstaller

echo.
echo Building executable...

REM Build WITHOUT Playwright to avoid JS errors
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "CookieChecker" ^
    --add-data "configs;configs" ^
    --hidden-import=httpx ^
    --hidden-import=orjson ^
    --hidden-import=h2 ^
    --hidden-import=selenium ^
    --hidden-import=undetected_chromedriver ^
    --exclude-module=playwright ^
    --exclude-module=playwright_stealth ^
    --optimize=2 ^
    --noconfirm ^
    gui.py

echo.
if exist "dist\CookieChecker.exe" (
    echo ✅ Build Complete!
    echo 📁 File: dist\CookieChecker.exe
) else (
    echo ❌ Build Failed!
)

pause
