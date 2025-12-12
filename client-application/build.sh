#!/bin/bash
# Build script for Linux/macOS
# Compiles the Cython extension

echo "========================================"
echo "Building Cython Extension"
echo "========================================"

# Check Python version
python3 --version

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Build the Cython extension
echo ""
echo "Building Cython extension..."
python3 setup.py build_ext --inplace

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Build successful!"
    echo "========================================"
    echo ""
    echo "The compiled extension is in the core/ directory."
    echo "You can now run: python3 main.py"
else
    echo ""
    echo "========================================"
    echo "Build failed!"
    echo "========================================"
fi
