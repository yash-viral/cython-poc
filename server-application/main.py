#!/usr/bin/env python3
"""
License Generator - Server Application
Main entry point for the license generation tool.
"""

import sys
from pathlib import Path

# Add the current directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

from controllers.license_controller import LicenseController


def main():
    """Main entry point."""
    controller = LicenseController()
    controller.run()


if __name__ == "__main__":
    main()
