"""
Business Service - Core business logic (protected by license).
This service contains the main application logic.
"""


class BusinessService:
    """
    Core business logic service.
    This is a simple example that prints "Hello World".
    In a real application, this would contain your protected business logic.
    """
    
    def __init__(self, customer_name: str = "Unknown"):
        self.customer_name = customer_name
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize the business service."""
        print(f"[BusinessService] Initializing for customer: {self.customer_name}")
        self._initialized = True
    
    def execute(self) -> str:
        """
        Execute the main business logic.
        
        Returns:
            Result message
        """
        if not self._initialized:
            raise RuntimeError("BusinessService not initialized")
        
        # ============================================
        # YOUR PROTECTED BUSINESS LOGIC GOES HERE
        # This is the code that should be protected
        # by the license and Cython compilation
        # ============================================
        
        result = self._core_logic()
        
        return result
    
    def _core_logic(self) -> str:
        """
        Core business logic implementation.
        This method contains the actual business logic.
        """
        # Simple example: Hello World
        message = f"Hello World! Welcome, {self.customer_name}!"
        print(f"[BusinessService] {message}")
        return message
    
    def shutdown(self) -> None:
        """Cleanup and shutdown the service."""
        print(f"[BusinessService] Shutting down...")
        self._initialized = False
