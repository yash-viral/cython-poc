"""
Application Controller - Main application entry point.
Handles license validation and application startup.
"""

import sys
from typing import Optional

from models.license_model import LicenseStatus
from services.license_service import LicenseService
from services.business_service import BusinessService


class AppController:
    """Main application controller."""
    
    def __init__(
        self,
        license_path: str = "license.lic",
        pubkey_path: str = "pub.pem"
    ):
        self.license_path = license_path
        self.pubkey_path = pubkey_path
        self.license_service: Optional[LicenseService] = None
        self.business_service: Optional[BusinessService] = None
        self.protected_module = None
    
    def run(self) -> int:
        """
        Run the application.
        
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        print("=" * 50)
        print("Licensed Application Starting...")
        print("=" * 50)
        
        # Step 1: Validate license
        if not self._validate_license():
            return 1
        
        # Step 2: Import and run protected module
        if not self._load_protected_module():
            print("Warning: Protected module not available (not compiled)")
            print("Running with standard Python module instead...")
        
        # Step 3: Execute business logic
        return self._execute_business_logic()
    
    def _validate_license(self) -> bool:
        """
        Validate the license.
        
        Returns:
            True if license is valid, False otherwise
        """
        print("\n[1/3] Validating license...")
        
        # Try to get embedded public key from protected module
        embedded_pubkey = None
        try:
            from core.protected_module import get_embedded_pubkey
            embedded_pubkey = get_embedded_pubkey()
        except ImportError:
            pass
        
        self.license_service = LicenseService(
            license_path=self.license_path,
            pubkey_path=self.pubkey_path,
            embedded_pubkey=embedded_pubkey
        )
        
        status, message, license_obj = self.license_service.validate_license()
        
        if status == LicenseStatus.VALID:
            print(f"✓ {message}")
            # Store customer name for business service
            if license_obj:
                self._customer_name = license_obj.customer
            return True
        else:
            print(f"✗ License validation failed: {message}")
            print(f"  Status code: {status.value}")
            sys.exit(status.value)
            return False
    
    def _load_protected_module(self) -> bool:
        """
        Load the Cython-compiled protected module.
        
        Returns:
            True if module loaded successfully
        """
        print("\n[2/3] Loading protected module...")
        
        try:
            from core import protected_module
            self.protected_module = protected_module
            print("✓ Protected module loaded successfully")
            return True
        except ImportError as e:
            print(f"⚠ Could not load protected module: {e}")
            return False
    
    def _execute_business_logic(self) -> int:
        """
        Execute the main business logic.
        
        Returns:
            Exit code
        """
        print("\n[3/3] Executing business logic...")
        print("-" * 50)
        
        customer_name = getattr(self, '_customer_name', 'Unknown Customer')
        
        try:
            if self.protected_module:
                # Use the Cython-compiled protected module
                print("\n--- Using Protected Module ---")
                
                # Call the simple hello_world function
                result = self.protected_module.hello_world()
                
                # Use the protected business logic class
                logic = self.protected_module.ProtectedBusinessLogic(customer_name)
                logic.start()
                result = logic.execute_protected_logic()
                logic.stop()
                
            else:
                # Fallback to standard Python business service
                print("\n--- Using Standard Business Service ---")
                self.business_service = BusinessService(customer_name)
                self.business_service.initialize()
                result = self.business_service.execute()
                self.business_service.shutdown()
            
            print("-" * 50)
            print("\n✓ Business logic executed successfully!")
            return 0
            
        except Exception as e:
            print(f"\n✗ Error executing business logic: {e}")
            return 1
