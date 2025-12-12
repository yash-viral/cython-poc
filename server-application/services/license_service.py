"""
License Service - Business logic for license generation.
"""

import json
from pathlib import Path
from typing import Optional

from models.license_model import License, LicenseBindings
from utils.crypto_utils import CryptoUtils


class LicenseService:
    """Service for license generation and management."""
    
    def __init__(
        self,
        keys_dir: str = "keys",
        licenses_dir: str = "licenses"
    ):
        self.keys_dir = Path(keys_dir)
        self.licenses_dir = Path(licenses_dir)
        self.crypto = CryptoUtils()
        
        # Ensure directories exist
        self.keys_dir.mkdir(parents=True, exist_ok=True)
        self.licenses_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def public_key_path(self) -> Path:
        return self.keys_dir / "pub.pem"
    
    @property
    def private_key_path(self) -> Path:
        return self.keys_dir / "priv.pem"
    
    def keys_exist(self) -> bool:
        """Check if RSA keys already exist."""
        return self.public_key_path.exists() and self.private_key_path.exists()
    
    def generate_keys(self, force: bool = False) -> tuple[str, str]:
        """
        Generate RSA key pair.
        
        Args:
            force: If True, overwrite existing keys
            
        Returns:
            Tuple of (public_key_path, private_key_path)
            
        Raises:
            FileExistsError: If keys exist and force is False
        """
        if self.keys_exist() and not force:
            raise FileExistsError(
                "Keys already exist. Use --force to overwrite."
            )
        
        return self.crypto.generate_rsa_keypair(
            str(self.public_key_path),
            str(self.private_key_path)
        )
    
    def create_license(
        self,
        customer: str,
        expiry: str,
        bind_mac: Optional[list[str]] = None,
        bind_hostname: Optional[list[str]] = None,
        output_path: Optional[str] = None
    ) -> License:
        """
        Create a signed license.
        
        Args:
            customer: Customer name
            expiry: Expiry date in ISO format (YYYY-MM-DD)
            bind_mac: List of allowed MAC addresses
            bind_hostname: List of allowed hostnames
            output_path: Path to save license file
            
        Returns:
            Signed License object
        """
        if not self.keys_exist():
            raise FileNotFoundError(
                "RSA keys not found. Run 'genkeys' first."
            )
        
        # Create bindings
        bindings = LicenseBindings(
            mac=bind_mac or [],
            host=bind_hostname or []
        )
        
        # Create license
        license_obj = License(
            customer=customer,
            expiry=expiry,
            bindings=bindings
        )
        
        # Load private key and sign
        private_key = self.crypto.load_private_key(str(self.private_key_path))
        payload = license_obj.get_payload()
        license_obj.signature = self.crypto.sign_data(payload, private_key)
        
        # Save to file
        if output_path:
            output_file = Path(output_path)
        else:
            # Generate filename based on customer
            safe_customer = "".join(
                c if c.isalnum() else "_" for c in customer
            ).lower()
            output_file = self.licenses_dir / f"{safe_customer}.lic"
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w") as f:
            json.dump(license_obj.to_license_file(), f, indent=2)
        
        return license_obj
    
    def verify_license(self, license_path: str) -> tuple[bool, str]:
        """
        Verify a license file signature.
        
        Args:
            license_path: Path to license file
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            with open(license_path, "r") as f:
                data = json.load(f)
            
            license_obj = License.from_license_file(data)
            
            # Load public key
            public_key = self.crypto.load_public_key(str(self.public_key_path))
            
            # Verify signature
            is_valid = self.crypto.verify_signature(
                license_obj.get_payload(),
                license_obj.signature,
                public_key
            )
            
            if not is_valid:
                return False, "Invalid signature"
            
            if license_obj.is_expired():
                return False, f"License expired on {license_obj.expiry}"
            
            return True, f"License valid for {license_obj.customer}"
            
        except Exception as e:
            return False, f"Verification error: {str(e)}"
