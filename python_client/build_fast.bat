@echo off
echo ========================================
echo Building High-Performance Standalone
echo ========================================
echo.

echo [1/4] Installing dependencies...
pip install -r requirements_fast.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Installing PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo [3/4] Building executable...
pyinstaller --onefile --windowed ^
    --name "CookieChecker-Fast" ^
    --add-data "configs;configs" ^
    --hidden-import=httpx ^
    --hidden-import=orjson ^
    --hidden-import=h2 ^
    --hidden-import=httpx._transports.default ^
    --hidden-import=httpx._transports.asgi ^
    --hidden-import=httpcore ^
    --collect-all customtkinter ^
    --optimize=2 ^
    standalone_gui.py

if %errorlevel% neq 0 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo [4/4] Cleaning up...
rmdir /s /q build 2>nul

echo.
echo ========================================
echo Build complete!
echo ========================================
echo Executable: dist\CookieChecker-Fast.exe
echo.
pause
