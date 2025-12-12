#!/usr/bin/env python3
"""
Licensed Application - Client Application
Main entry point for the licensed application.
"""

import sys
import argparse
from pathlib import Path

# Add the current directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

from controllers.app_controller import AppController


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="licensed-app",
        description="Licensed Application with Cython Protection"
    )
    parser.add_argument(
        "--lic",
        default="license.lic",
        help="Path to license file"
    )
    parser.add_argument(
        "--pub",
        default="pub.pem",
        help="Path to public key file"
    )
    
    args = parser.parse_args()
    
    controller = AppController(
        license_path=args.lic,
        pubkey_path=args.pub
    )
    
    exit_code = controller.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
