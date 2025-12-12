"""
License Service - Business logic for license validation.
"""

import json
import base64
from pathlib import Path
from typing import Tuple, Optional

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from models.license_model import License, LicenseStatus
from utils.machine_utils import MachineUtils


class LicenseService:
    """Service for license validation."""
    
    def __init__(
        self,
        license_path: str = "license.lic",
        pubkey_path: str = "pub.pem",
        embedded_pubkey: Optional[str] = None
    ):
        self.license_path = Path(license_path)
        self.pubkey_path = Path(pubkey_path)
        self.embedded_pubkey = embedded_pubkey
        self.machine = MachineUtils()
    
    def get_public_key(self) -> bytes:
        """
        Get the public key for verification.
        Uses embedded key if available, otherwise reads from file.
        """
        if self.embedded_pubkey:
            return self.embedded_pubkey.encode('utf-8')
        
        with open(self.pubkey_path, "rb") as f:
            return f.read()
    
    def load_license(self) -> License:
        """Load license from file."""
        if not self.license_path.exists():
            raise FileNotFoundError(f"License file not found: {self.license_path}")
        
        with open(self.license_path, "r") as f:
            data = json.load(f)
        
        return License.from_license_file(data)
    
    def verify_signature(self, license_obj: License) -> bool:
        """
        Verify the license signature using RSA public key.
        
        Args:
            license_obj: License object to verify
            
        Returns:
            True if signature is valid
        """
        try:
            pubkey_pem = self.get_public_key()
            public_key = RSA.import_key(pubkey_pem)
            
            payload = license_obj.get_payload()
            json_str = json.dumps(payload, sort_keys=True)
            h = SHA256.new(json_str.encode('utf-8'))
            
            signature = base64.b64decode(license_obj.signature)
            pkcs1_15.new(public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False
    
    def check_mac_binding(self, license_obj: License) -> bool:
        """
        Check if current machine MAC matches license binding.
        
        Args:
            license_obj: License object
            
        Returns:
            True if MAC matches or no MAC binding exists
        """
        allowed_macs = [m.lower() for m in license_obj.bindings.mac]
        if not allowed_macs:
            return True  # No MAC binding
        
        current_mac = self.machine.get_primary_mac()
        return current_mac in allowed_macs
    
    def check_hostname_binding(self, license_obj: License) -> bool:
        """
        Check if current hostname matches license binding.
        
        Args:
            license_obj: License object
            
        Returns:
            True if hostname matches or no hostname binding exists
        """
        allowed_hosts = [h.lower() for h in license_obj.bindings.host]
        if not allowed_hosts:
            return True  # No hostname binding
        
        current_host = self.machine.get_hostname()
        return current_host in allowed_hosts
    
    def validate_license(self, require_bindings: bool = True) -> Tuple[LicenseStatus, str, Optional[License]]:
        """
        Perform full license validation.
        
        Args:
            require_bindings: If True, validate machine bindings
            
        Returns:
            Tuple of (status, message, license_object or None)
        """
        try:
            # Load license
            license_obj = self.load_license()
        except FileNotFoundError as e:
            return LicenseStatus.FILE_NOT_FOUND, str(e), None
        except json.JSONDecodeError:
            return LicenseStatus.INVALID_FORMAT, "Invalid license file format", None
        except Exception as e:
            return LicenseStatus.UNKNOWN_ERROR, f"Error loading license: {e}", None
        
        # Verify signature
        if not self.verify_signature(license_obj):
            return LicenseStatus.INVALID_SIGNATURE, "Invalid license signature", None
        
        # Check expiry
        if license_obj.is_expired():
            return (
                LicenseStatus.EXPIRED,
                f"License expired on {license_obj.expiry}",
                license_obj
            )
        
        # Check bindings if required
        if require_bindings and license_obj.bindings.has_bindings():
            # Check MAC binding
            if license_obj.bindings.mac and not self.check_mac_binding(license_obj):
                current_mac = self.machine.get_primary_mac()
                return (
                    LicenseStatus.MAC_MISMATCH,
                    f"MAC mismatch. Current: {current_mac}, Allowed: {license_obj.bindings.mac}",
                    license_obj
                )
            
            # Check hostname binding
            if license_obj.bindings.host and not self.check_hostname_binding(license_obj):
                current_host = self.machine.get_hostname()
                return (
                    LicenseStatus.HOSTNAME_MISMATCH,
                    f"Hostname mismatch. Current: {current_host}, Allowed: {license_obj.bindings.host}",
                    license_obj
                )
        
        # All checks passed
        days_left = license_obj.days_until_expiry()
        message = f"License valid for {license_obj.customer}. Expires in {days_left} days."
        return LicenseStatus.VALID, message, license_obj
