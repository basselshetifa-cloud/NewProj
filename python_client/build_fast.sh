#!/bin/bash

echo "========================================"
echo "Building High-Performance Standalone"
echo "========================================"
echo ""

# Validate required files exist
echo "[0/5] Validating files..."
if [ ! -f "standalone_gui.py" ]; then
    echo "ERROR: standalone_gui.py not found"
    exit 1
fi

if [ ! -f "requirements_fast.txt" ]; then
    echo "ERROR: requirements_fast.txt not found"
    exit 1
fi

# Determine configs path
CONFIGS_PATH=""
if [ -d "configs" ]; then
    CONFIGS_PATH="configs"
elif [ -d "../configs" ]; then
    CONFIGS_PATH="../configs"
else
    echo "ERROR: configs directory not found"
    exit 1
fi

echo "  ✓ All required files found"
echo "  ✓ Using configs from: $CONFIGS_PATH"

echo ""
echo "[1/5] Installing dependencies..."
pip3 install -r requirements_fast.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[2/5] Installing PyInstaller..."
pip3 install pyinstaller
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install PyInstaller"
    exit 1
fi

echo ""
echo "[3/5] Building executable..."
pyinstaller --onefile --windowed \
    --name "CookieChecker-Fast" \
    --add-data "${CONFIGS_PATH}:configs" \
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
echo "[4/5] Cleaning up and setting permissions..."
rm -rf build
chmod +x dist/CookieChecker-Fast

echo ""
echo "[5/5] Verifying executable..."
if [ ! -f "dist/CookieChecker-Fast" ]; then
    echo "ERROR: Executable not found at dist/CookieChecker-Fast"
    exit 1
fi

echo "  ✓ Executable created successfully"

echo ""
echo "========================================"
echo "Build complete!"
echo "========================================"
echo "Executable: dist/CookieChecker-Fast"
echo ""
