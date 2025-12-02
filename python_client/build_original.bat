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
    --add-data "configs;configs" ^
    --optimize=2 ^
    --noconfirm ^
    cookie_checker.py

echo.
if exist "dist\CookieChecker-Original.exe" (
    echo ✅ Build Complete!
    echo 📁 File: dist\CookieChecker-Original.exe
    echo.
    echo 🎯 Features:
    echo    - Dynamic config loading from configs/
    echo    - 4-column checkbox grid
    echo    - Multi-threaded scanning (50 threads)
    echo    - Real-time CPM tracking
) else (
    echo ❌ Build Failed!
)

pause
