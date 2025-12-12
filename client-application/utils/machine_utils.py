"""
Machine Utilities - Functions for machine identification.
Used for license binding verification.
"""

import uuid
import socket
from typing import Optional


class MachineUtils:
    """Utility class for machine identification."""
    
    @staticmethod
    def get_primary_mac() -> str:
        """
        Get the primary MAC address of the machine.
        
        Returns:
            MAC address as string in format AA:BB:CC:DD:EE:FF
        """
        mac_int = uuid.getnode()
        mac = ':'.join(
            f"{(mac_int >> offset) & 0xff:02x}"
            for offset in range(40, -8, -8)
        )
        return mac.lower()
    
    @staticmethod
    def get_hostname() -> str:
        """
        Get the hostname of the machine.
        
        Returns:
            Hostname as string
        """
        return socket.gethostname().lower()
    
    @staticmethod
    def get_all_mac_addresses() -> list[str]:
        """
        Get all MAC addresses from the machine.
        This is useful for machines with multiple network interfaces.
        
        Returns:
            List of MAC addresses
        """
        # For simplicity, we only return the primary MAC
        # In production, you might want to enumerate all interfaces
        return [MachineUtils.get_primary_mac()]
    
    @staticmethod
    def get_machine_fingerprint() -> dict:
        """
        Get a fingerprint of the machine.
        
        Returns:
            Dictionary with machine identifiers
        """
        return {
            "mac": MachineUtils.get_primary_mac(),
            "hostname": MachineUtils.get_hostname()
        }
