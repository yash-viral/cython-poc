"""
Setup script for building Cython extensions.
Run: python setup.py build_ext --inplace
"""

from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import sys
import os

# Cython extensions to build
extensions = [
    Extension(
        "core.protected_module",
        ["core/protected_module.pyx"],
        extra_compile_args=["-O3"],  # Optimization level
    )
]

# Compiler directives for Cython
compiler_directives = {
    'language_level': "3",
    'embedsignature': False,  # Don't embed signatures (harder to reverse)
    'boundscheck': False,     # Disable bounds checking for speed
    'wraparound': False,      # Disable negative indexing for speed
}

setup(
    name="licensed-app",
    version="1.0.0",
    description="Licensed Application with Cython Protection",
    packages=find_packages(),
    ext_modules=cythonize(
        extensions,
        compiler_directives=compiler_directives,
        annotate=False,  # Don't generate HTML annotation files
    ),
    python_requires=">=3.12",
    install_requires=[
        "pycryptodome>=3.20.0",
    ],
    zip_safe=False,
)
