@echo off
REM Quick test script for local obfuscation testing

echo ========================================
echo CYTHON OBFUSCATION LOCAL TEST
echo ========================================
echo.

echo This script will:
echo 1. Build the Cython extension
echo 2. Generate keys and license
echo 3. Test the obfuscated code
echo 4. Show obfuscation comparison
echo.

pause

echo Running full obfuscation test...
python test_obfuscation.py

echo.
echo ========================================
echo SHOWING OBFUSCATION COMPARISON
echo ========================================
echo.

python compare_obfuscation.py

echo.
echo ========================================
echo TEST COMPLETE
echo ========================================
echo.
echo Check the output above to see:
echo - How your .pyx source code gets compiled to binary
echo - What methods are hidden from Python access
echo - The difference between source and compiled code
echo.

pause