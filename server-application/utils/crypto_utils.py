"""
Cryptographic utilities for license generation.
Handles RSA key generation and signing operations.
"""

import json
import base64
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class CryptoUtils:
    """Utility class for cryptographic operations."""
    
    DEFAULT_KEY_SIZE = 4096
    
    @staticmethod
    def generate_rsa_keypair(
        pub_path: str = "keys/pub.pem",
        priv_path: str = "keys/priv.pem",
        key_size: int = DEFAULT_KEY_SIZE
    ) -> tuple[str, str]:
        """
        Generate RSA key pair and save to files.
        
        Args:
            pub_path: Path to save public key
            priv_path: Path to save private key
            key_size: RSA key size in bits
            
        Returns:
            Tuple of (public_key_path, private_key_path)
        """
        # Ensure directories exist
        Path(pub_path).parent.mkdir(parents=True, exist_ok=True)
        Path(priv_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Generate key pair
        key = RSA.generate(key_size)
        
        # Save private key
        with open(priv_path, "wb") as f:
            f.write(key.export_key())
        
        # Save public key
        with open(pub_path, "wb") as f:
            f.write(key.publickey().export_key())
        
        return pub_path, priv_path
    
    @staticmethod
    def load_private_key(priv_path: str) -> RSA.RsaKey:
        """Load RSA private key from file."""
        with open(priv_path, "rb") as f:
            return RSA.import_key(f.read())
    
    @staticmethod
    def load_public_key(pub_path: str) -> RSA.RsaKey:
        """Load RSA public key from file."""
        with open(pub_path, "rb") as f:
            return RSA.import_key(f.read())
    
    @staticmethod
    def sign_data(data: dict, private_key: RSA.RsaKey) -> str:
        """
        Sign dictionary data with RSA private key.
        
        Args:
            data: Dictionary to sign (will be JSON serialized)
            private_key: RSA private key
            
        Returns:
            Base64-encoded signature
        """
        # Create deterministic JSON string
        json_str = json.dumps(data, sort_keys=True)
        
        # Hash the data
        h = SHA256.new(json_str.encode('utf-8'))
        
        # Sign the hash
        signature = pkcs1_15.new(private_key).sign(h)
        
        # Return base64-encoded signature
        return base64.b64encode(signature).decode('utf-8')
    
    @staticmethod
    def verify_signature(data: dict, signature_b64: str, public_key: RSA.RsaKey) -> bool:
        """
        Verify signature of dictionary data.
        
        Args:
            data: Dictionary that was signed
            signature_b64: Base64-encoded signature
            public_key: RSA public key
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            json_str = json.dumps(data, sort_keys=True)
            h = SHA256.new(json_str.encode('utf-8'))
            signature = base64.b64decode(signature_b64)
            pkcs1_15.new(public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False
