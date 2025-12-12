#!/bin/bash
# Quick test script for Linux/macOS
# Tests the complete flow: generate keys -> create license -> run app

echo "========================================"
echo "Cython Licensing POC - Quick Test"
echo "========================================"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Step 1: Setup Server
echo ""
echo "[Step 1/4] Setting up server application..."
cd "$SCRIPT_DIR/server-application"
pip3 install -r requirements.txt -q

# Step 2: Generate Keys
echo ""
echo "[Step 2/4] Generating RSA keys..."
python3 main.py genkeys --force

# Step 3: Create License
echo ""
echo "[Step 3/4] Creating test license..."
python3 main.py create --customer "Test Customer" --expiry 2026-12-31 --out "../client-application/license.lic"

# Copy public key to client
cp keys/pub.pem "../client-application/pub.pem"

# Step 4: Run Client (without Cython compilation for quick test)
echo ""
echo "[Step 4/4] Running client application..."
cd "$SCRIPT_DIR/client-application"
pip3 install pycryptodome -q
python3 main.py

echo ""
echo "========================================"
echo "Quick test complete!"
echo "========================================"
echo ""
echo "To build with Cython protection:"
echo "  cd client-application"
echo "  ./build.sh"
echo "  python3 main.py"
