@echo off
REM Build script for Windows
REM Compiles the Cython extension

echo ========================================
echo Building Cython Extension
echo ========================================

REM Check Python version
python --version

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Build the Cython extension
echo.
echo Building Cython extension...
python setup.py build_ext --inplace

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Build successful!
    echo ========================================
    echo.
    echo The compiled extension is in the core/ directory.
    echo You can now run: python main.py
) else (
    echo.
    echo ========================================
    echo Build failed!
    echo ========================================
)
