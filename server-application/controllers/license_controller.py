"""
License Controller - Handles CLI interface for license operations.
"""

import argparse
import sys
from typing import Optional

from services.license_service import LicenseService


class LicenseController:
    """Controller for license generation CLI."""
    
    def __init__(self):
        self.service = LicenseService()
    
    def run(self, args: Optional[list[str]] = None):
        """Run the CLI application."""
        parser = self._create_parser()
        parsed_args = parser.parse_args(args)
        
        if not hasattr(parsed_args, 'command') or parsed_args.command is None:
            parser.print_help()
            sys.exit(1)
        
        try:
            if parsed_args.command == "genkeys":
                self._handle_genkeys(parsed_args)
            elif parsed_args.command == "create":
                self._handle_create(parsed_args)
            elif parsed_args.command == "verify":
                self._handle_verify(parsed_args)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            prog="license-generator",
            description="Generate and manage software licenses"
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Commands")
        
        # genkeys command
        genkeys_parser = subparsers.add_parser(
            "genkeys",
            help="Generate RSA key pair"
        )
        genkeys_parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing keys"
        )
        
        # create command
        create_parser = subparsers.add_parser(
            "create",
            help="Create a new license"
        )
        create_parser.add_argument(
            "--customer",
            required=True,
            help="Customer name"
        )
        create_parser.add_argument(
            "--expiry",
            required=True,
            help="Expiry date (YYYY-MM-DD)"
        )
        create_parser.add_argument(
            "--out",
            help="Output file path"
        )
        create_parser.add_argument(
            "--bind-mac",
            nargs="*",
            help="Bind to MAC address(es)"
        )
        create_parser.add_argument(
            "--bind-hostname",
            nargs="*",
            help="Bind to hostname(s)"
        )
        
        # verify command
        verify_parser = subparsers.add_parser(
            "verify",
            help="Verify a license file"
        )
        verify_parser.add_argument(
            "--lic",
            required=True,
            help="Path to license file"
        )
        
        return parser
    
    def _handle_genkeys(self, args):
        """Handle genkeys command."""
        pub_path, priv_path = self.service.generate_keys(force=args.force)
        print(f"Generated RSA key pair:")
        print(f"  Public key:  {pub_path}")
        print(f"  Private key: {priv_path}")
        print("\nKeep the private key secure! Distribute the public key with your application.")
    
    def _handle_create(self, args):
        """Handle create command."""
        license_obj = self.service.create_license(
            customer=args.customer,
            expiry=args.expiry,
            bind_mac=args.bind_mac,
            bind_hostname=args.bind_hostname,
            output_path=args.out
        )
        
        print(f"License created successfully!")
        print(f"  Customer: {license_obj.customer}")
        print(f"  Expiry:   {license_obj.expiry}")
        
        if license_obj.bindings.mac:
            print(f"  MAC bindings: {', '.join(license_obj.bindings.mac)}")
        if license_obj.bindings.host:
            print(f"  Host bindings: {', '.join(license_obj.bindings.host)}")
        
        if args.out:
            print(f"  Output: {args.out}")
    
    def _handle_verify(self, args):
        """Handle verify command."""
        is_valid, message = self.service.verify_license(args.lic)
        
        if is_valid:
            print(f"✓ {message}")
            sys.exit(0)
        else:
            print(f"✗ {message}")
            sys.exit(1)
