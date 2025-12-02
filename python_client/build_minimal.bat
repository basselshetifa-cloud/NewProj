@echo off
echo ========================================
echo Building Minimal Standalone (No Playwright)
echo ========================================
echo.

echo [0/5] Validating files...
if not exist "standalone_gui_minimal.py" (
    echo ERROR: standalone_gui_minimal.py not found
    pause
    exit /b 1
)

if not exist "requirements_fast.txt" (
    echo ERROR: requirements_fast.txt not found
    pause
    exit /b 1
)

REM Determine configs path
set CONFIGS_PATH=
if exist "configs" (
    set CONFIGS_PATH=configs
) else if exist "..\configs" (
    set CONFIGS_PATH=..\configs
) else (
    echo ERROR: configs directory not found
    pause
    exit /b 1
)

echo   √ All required files found
echo   √ Using configs from: %CONFIGS_PATH%

echo.
echo [1/5] Installing dependencies (excluding playwright)...
pip install customtkinter httpx[http2] h2 orjson aiofiles selenium undetected-chromedriver webdriver-manager Pillow
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/5] Installing PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo [3/5] Building minimal executable (no Playwright)...
pyinstaller --onefile --windowed ^
    --name "CookieChecker-Minimal" ^
    --add-data "%CONFIGS_PATH%;configs" ^
    --hidden-import=httpx ^
    --hidden-import=orjson ^
    --hidden-import=h2 ^
    --hidden-import=httpx._transports.default ^
    --hidden-import=httpx._transports.asgi ^
    --hidden-import=httpcore ^
    --hidden-import=selenium ^
    --hidden-import=undetected_chromedriver ^
    --collect-all customtkinter ^
    --optimize=2 ^
    standalone_gui_minimal.py

if %errorlevel% neq 0 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo [4/5] Cleaning up...
rmdir /s /q build 2>nul

echo.
echo [5/5] Verifying executable...
if not exist "dist\CookieChecker-Minimal.exe" (
    echo ERROR: Executable not found at dist\CookieChecker-Minimal.exe
    pause
    exit /b 1
)

echo   √ Executable created successfully

echo.
echo ========================================
echo Minimal Build Complete!
echo ========================================
echo Executable: dist\CookieChecker-Minimal.exe
echo.
echo Includes: Fast Python + Multi-Process + Selenium
echo Does NOT include: Playwright (avoids JS file issues)
echo.
pause
