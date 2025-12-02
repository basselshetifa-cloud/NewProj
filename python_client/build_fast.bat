@echo off
echo ========================================
echo Building High-Performance Standalone
echo ========================================
echo.

echo [0/5] Validating files...
if not exist "standalone_gui.py" (
    echo ERROR: standalone_gui.py not found
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
echo [1/5] Installing dependencies...
pip install -r requirements_fast.txt
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
echo [3/5] Building executable...

REM Find playwright-stealth installation path
set STEALTH_PATH=
for /f "delims=" %%i in ('python -c "try: import playwright_stealth, os; print(os.path.dirname(playwright_stealth.__file__))\nexcept: pass"') do set STEALTH_PATH=%%i

if defined STEALTH_PATH (
    echo   √ Found playwright-stealth at: %STEALTH_PATH%
    pyinstaller --onefile --windowed ^
        --name "CookieChecker-Fast" ^
        --add-data "%CONFIGS_PATH%;configs" ^
        --add-data "%STEALTH_PATH%;playwright_stealth" ^
        --hidden-import=httpx ^
        --hidden-import=orjson ^
        --hidden-import=h2 ^
        --hidden-import=httpx._transports.default ^
        --hidden-import=httpx._transports.asgi ^
        --hidden-import=httpcore ^
        --hidden-import=playwright ^
        --hidden-import=playwright_stealth ^
        --hidden-import=selenium ^
        --hidden-import=undetected_chromedriver ^
        --collect-all customtkinter ^
        --collect-all playwright_stealth ^
        --collect-all playwright ^
        --optimize=2 ^
        standalone_gui.py
) else (
    echo   ! Playwright-stealth not found - building without it
    pyinstaller --onefile --windowed ^
        --name "CookieChecker-Fast" ^
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
        standalone_gui.py
)

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
if not exist "dist\CookieChecker-Fast.exe" (
    echo ERROR: Executable not found at dist\CookieChecker-Fast.exe
    pause
    exit /b 1
)

echo   √ Executable created successfully

echo.
echo ========================================
echo Build complete!
echo ========================================
echo Executable: dist\CookieChecker-Fast.exe
echo.
pause
