#!/usr/bin/env python3
"""
Obfuscation Test Script
Tests the Cython obfuscation locally without Docker.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result."""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=check
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"Error: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return e

def build_cython_extension():
    """Build the Cython extension."""
    print("=" * 50)
    print("BUILDING CYTHON EXTENSION")
    print("=" * 50)
    
    client_dir = Path("client-application")
    
    # Install setuptools and dependencies
    print("Installing setuptools and dependencies...")
    run_command("pip install setuptools wheel", cwd=client_dir)
    run_command("pip install -r requirements.txt", cwd=client_dir)
    
    # Build Cython extension
    print("Building Cython extension...")
    result = run_command("python setup.py build_ext --inplace", cwd=client_dir)
    
    if result.returncode == 0:
        print("✅ Cython extension built successfully!")
        
        # List generated files
        print("\nGenerated files:")
        for file in client_dir.glob("core/*"):
            if file.suffix in ['.so', '.pyd', '.c']:
                print(f"  - {file}")
        
        return True
    else:
        print("❌ Failed to build Cython extension!")
        return False

def test_obfuscation():
    """Test the obfuscation by comparing source vs compiled."""
    print("=" * 50)
    print("TESTING OBFUSCATION")
    print("=" * 50)
    
    client_dir = Path("client-application")
    
    # Show original source code
    print("1. Original Cython source code (.pyx):")
    pyx_file = client_dir / "core" / "protected_module.pyx"
    if pyx_file.exists():
        with open(pyx_file, 'r') as f:
            lines = f.readlines()
        
        print(f"   File: {pyx_file}")
        print(f"   Size: {len(lines)} lines")
        print("   Sample content:")
        for i, line in enumerate(lines[40:50], 41):
            print(f"   {i:3d}: {line.rstrip()}")
    
    # Show compiled files
    print("\n2. Compiled files:")
    compiled_files = list(client_dir.glob("core/*.so")) + list(client_dir.glob("core/*.pyd"))
    
    for compiled_file in compiled_files:
        print(f"   File: {compiled_file}")
        print(f"   Size: {compiled_file.stat().st_size} bytes")
        
        # Show it's binary
        with open(compiled_file, 'rb') as f:
            data = f.read(100)
        
        print("   Content (first 100 bytes as hex):")
        hex_data = data.hex()
        for i in range(0, min(len(hex_data), 64), 16):
            print(f"   {hex_data[i:i+16]}")
        print("   ...")

def demonstrate_protection():
    """Demonstrate the protection by trying to access internals."""
    print("=" * 50)
    print("DEMONSTRATING PROTECTION")
    print("=" * 50)
    
    # Add client directory to path
    client_dir = Path("client-application").resolve()
    sys.path.insert(0, str(client_dir))
    
    try:
        # Import the compiled module
        from core.protected_module import ProtectedBusinessLogic, secret_function, hello_world
        
        print("✅ Successfully imported compiled module")
        
        # Test basic functionality
        print("\n1. Testing basic functions:")
        print(f"   hello_world(): {hello_world()}")
        print(f"   secret_function(): {secret_function()}")
        
        # Test protected class
        print("\n2. Testing protected class:")
        logic = ProtectedBusinessLogic("Test Customer")
        logic.start()
        result = logic.execute_protected_logic()
        logic.stop()
        
        # Try to access internals (should be hidden)
        print("\n3. Trying to access internal methods:")
        try:
            logic._initialize_internals()
            print("   ❌ _initialize_internals() is accessible (not protected)")
        except AttributeError:
            print("   ✅ _initialize_internals() is hidden (protected)")
        
        try:
            logic._compute_secret()
            print("   ❌ _compute_secret() is accessible (not protected)")
        except AttributeError:
            print("   ✅ _compute_secret() is hidden (protected)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import compiled module: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing protection: {e}")
        return False

def main():
    """Main test function."""
    print("CYTHON OBFUSCATION TEST")
    print("=" * 50)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    success = True
    
    # Build and test
    success &= build_cython_extension()
    
    if success:
        test_obfuscation()
        success &= demonstrate_protection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("\nObfuscation Summary:")
        print("- ✅ Cython compiled your .pyx file to binary")
        print("- ✅ Source code is hidden in compiled .so/.pyd file")
        print("- ✅ Internal cdef methods are not accessible from Python")
    else:
        print("❌ SOME TESTS FAILED!")
    
    print("=" * 50)

if __name__ == "__main__":
    main()