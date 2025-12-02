@echo off
echo 🔥 Building Original Cookie Checker GUI
echo.

REM Install minimal dependencies
pip install customtkinter

echo.
echo Building executable...

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "CookieChecker-Original" ^
    --optimize=2 ^
    --noconfirm ^
    cookie_checker.py

echo.
if exist "dist\CookieChecker-Original.exe" (
    echo ✅ Build Complete!
    echo 📁 File: dist\CookieChecker-Original.exe
    echo.
    echo 🎯 Features:
    echo    - Simple keyword-based checking
    echo    - Multi-threaded scanning
    echo    - 22+ service support
    echo    - Real-time CPM tracking
) else (
    echo ❌ Build Failed!
)

pause
