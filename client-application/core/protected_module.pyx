# protected_module.pyx
# cython: language_level=3
"""
Protected Module - Compiled with Cython for code obfuscation.
This module contains critical business logic that should be protected.

The public key can optionally be embedded here to prevent easy tampering.
"""

# Optional: Embed public key directly in compiled module
# Replace this with your actual public key content
cdef str _EMBEDDED_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
REPLACE_WITH_YOUR_PUBLIC_KEY
-----END PUBLIC KEY-----
"""

# Flag to indicate if we should use embedded key
cdef bint _USE_EMBEDDED_KEY = False


def get_embedded_pubkey():
    """
    Get the embedded public key.
    
    Returns:
        Public key string if embedded, None otherwise
    """
    if _USE_EMBEDDED_KEY:
        return _EMBEDDED_PUBLIC_KEY
    return None


def set_use_embedded_key(use_embedded: bool):
    """
    Set whether to use the embedded public key.
    Call this during development/testing.
    """
    global _USE_EMBEDDED_KEY
    _USE_EMBEDDED_KEY = use_embedded


cdef class ProtectedBusinessLogic:
    """
    Protected business logic class.
    This class is compiled with Cython for obfuscation.
    """
    
    cdef str _customer_name
    cdef int _secret_value
    cdef bint _is_running
    
    def __init__(self, str customer_name):
        """Initialize with customer name."""
        self._customer_name = customer_name
        self._secret_value = 42  # Example secret data
        self._is_running = False
    
    def start(self):
        """Start the protected business logic."""
        if self._is_running:
            return
        
        print(f"[ProtectedModule] Starting for customer: {self._customer_name}")
        self._is_running = True
        self._initialize_internals()
    
    cdef void _initialize_internals(self):
        """Internal initialization (hidden from Python)."""
        # This method is only accessible from Cython, not Python
        self._secret_value = self._compute_secret()
    
    cdef int _compute_secret(self):
        """Compute a secret value (hidden from Python)."""
        cdef int result = 0
        cdef int i
        for i in range(100):
            result += i * self._secret_value
        return result % 1000
    
    def execute_protected_logic(self):
        """
        Execute the protected business logic.
        
        Returns:
            Result string
        """
        if not self._is_running:
            raise RuntimeError("ProtectedBusinessLogic not started")
        
        # ============================================
        # PROTECTED BUSINESS LOGIC
        # This code is compiled to a .so file
        # making it harder to reverse engineer
        # ============================================
        
        result = self._protected_computation()
        
        return result
    
    def _protected_computation(self):
        """
        The main protected computation.
        In a real application, this would contain your AI model loading,
        proprietary algorithms, etc.
        """
        # Example: Hello World with secret computation
        message = f"Hello World from Protected Module!"
        message += f"\nCustomer: {self._customer_name}"
        message += f"\nSecret computation result: {self._secret_value}"
        
        print(f"[ProtectedModule] {message}")
        return message
    
    def stop(self):
        """Stop the protected business logic."""
        if self._is_running:
            print(f"[ProtectedModule] Stopping...")
            self._is_running = False


def secret_function():
    """
    A simple secret function that can be called directly.
    This is compiled into the .so file.
    
    Returns:
        Secret message
    """
    return "Top secret model weights access: OK"


def hello_world():
    """
    Simple Hello World function - the main business logic.
    
    Returns:
        Hello World message
    """
    message = "Hello World from Cython Protected Module!"
    print(f"[ProtectedModule] {message}")
    return message
