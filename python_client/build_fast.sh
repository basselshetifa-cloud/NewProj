#!/bin/bash

echo "========================================"
echo "Building High-Performance Standalone"
echo "========================================"
echo ""

echo "[1/4] Installing dependencies..."
pip3 install -r requirements_fast.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[2/4] Installing PyInstaller..."
pip3 install pyinstaller
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install PyInstaller"
    exit 1
fi

echo ""
echo "[3/4] Building executable..."
pyinstaller --onefile --windowed \
    --name "CookieChecker-Fast" \
    --add-data "configs:configs" \
    --hidden-import=httpx \
    --hidden-import=orjson \
    --hidden-import=h2 \
    --hidden-import=httpx._transports.default \
    --hidden-import=httpx._transports.asgi \
    --hidden-import=httpcore \
    --collect-all customtkinter \
    --optimize=2 \
    standalone_gui.py

if [ $? -ne 0 ]; then
    echo "ERROR: Build failed"
    exit 1
fi

echo ""
echo "[4/4] Cleaning up and setting permissions..."
rm -rf build
chmod +x dist/CookieChecker-Fast

echo ""
echo "========================================"
echo "Build complete!"
echo "========================================"
echo "Executable: dist/CookieChecker-Fast"
echo ""
