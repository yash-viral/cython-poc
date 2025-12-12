"""
License Model - Data structure for license validation.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from enum import Enum


class LicenseStatus(Enum):
    """License validation status codes."""
    VALID = 0
    FILE_NOT_FOUND = 2
    INVALID_SIGNATURE = 3
    EXPIRED = 4
    MAC_MISMATCH = 5
    HOSTNAME_MISMATCH = 6
    INVALID_FORMAT = 7
    UNKNOWN_ERROR = 99


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
    
    def has_bindings(self) -> bool:
        """Check if there are any bindings."""
        return bool(self.mac or self.host)


@dataclass
class License:
    """License data model."""
    customer: str
    expiry: str  # ISO format date string (YYYY-MM-DD)
    bindings: LicenseBindings = field(default_factory=LicenseBindings)
    signature: Optional[str] = None
    
    def get_payload(self) -> dict:
        """Get the payload dictionary for verification."""
        return {
            "customer": self.customer,
            "expiry": self.expiry,
            "binds": self.bindings.to_dict()
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
    
    def get_expiry_date(self) -> datetime:
        """Get expiry as datetime object."""
        return datetime.fromisoformat(self.expiry)
    
    def is_expired(self) -> bool:
        """Check if license is expired."""
        return datetime.utcnow() > self.get_expiry_date()
    
    def days_until_expiry(self) -> int:
        """Get number of days until expiry (negative if expired)."""
        delta = self.get_expiry_date() - datetime.utcnow()
        return delta.days
    
    def __str__(self) -> str:
        return f"License(customer={self.customer}, expiry={self.expiry})"
