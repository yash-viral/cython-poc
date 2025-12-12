"""
License Model - Data structure for license information.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime


@dataclass
class LicenseBindings:
    """Machine bindings for license validation."""
    mac: list[str] = field(default_factory=list)
    host: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary, excluding empty lists."""
        result = {}
        if self.mac:
            result["mac"] = self.mac
        if self.host:
            result["host"] = self.host
        return result
    
    @classmethod
    def from_dict(cls, data: dict) -> "LicenseBindings":
        """Create from dictionary."""
        return cls(
            mac=data.get("mac", []),
            host=data.get("host", [])
        )


@dataclass
class License:
    """License data model."""
    customer: str
    expiry: str  # ISO format date string (YYYY-MM-DD)
    bindings: LicenseBindings = field(default_factory=LicenseBindings)
    signature: Optional[str] = None
    
    def get_payload(self) -> dict:
        """Get the payload dictionary for signing."""
        payload = {
            "customer": self.customer,
            "expiry": self.expiry,
            "binds": self.bindings.to_dict()
        }
        return payload
    
    def to_license_file(self) -> dict:
        """Convert to license file format."""
        return {
            "payload": self.get_payload(),
            "signature": self.signature
        }
    
    @classmethod
    def from_license_file(cls, data: dict) -> "License":
        """Create from license file format."""
        payload = data["payload"]
        return cls(
            customer=payload["customer"],
            expiry=payload["expiry"],
            bindings=LicenseBindings.from_dict(payload.get("binds", {})),
            signature=data.get("signature")
        )
    
    def is_expired(self) -> bool:
        """Check if license is expired."""
        expiry_date = datetime.fromisoformat(self.expiry)
        return datetime.utcnow() > expiry_date
    
    def __str__(self) -> str:
        return f"License(customer={self.customer}, expiry={self.expiry})"
