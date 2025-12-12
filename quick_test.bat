@echo off
REM Quick test script for Windows
REM Tests the complete flow: generate keys -> create license -> run app

echo ========================================
echo Cython Licensing POC - Quick Test
echo ========================================

REM Step 1: Setup Server
echo.
echo [Step 1/4] Setting up server application...
cd /d "%~dp0server-application"
pip install -r requirements.txt -q

REM Step 2: Generate Keys
echo.
echo [Step 2/4] Generating RSA keys...
python main.py genkeys --force

REM Step 3: Create License
echo.
echo [Step 3/4] Creating test license...
python main.py create --customer "Test Customer" --expiry 2026-12-31 --out "..\client-application\license.lic"

REM Copy public key to client
copy keys\pub.pem "..\client-application\pub.pem" > nul

REM Step 4: Run Client (without Cython compilation for quick test)
echo.
echo [Step 4/4] Running client application...
cd /d "%~dp0client-application"
pip install pycryptodome -q
python main.py

echo.
echo ========================================
echo Quick test complete!
echo ========================================
echo.
echo To build with Cython protection:
echo   cd client-application
echo   build.bat
echo   python main.py
