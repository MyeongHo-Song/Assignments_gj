"""
exceptions.py
Custom exceptions for the bank system
"""

class InvalidPasswordError(Exception):
    """Exception raised when password validation fails"""
    def __init__(self, message="Incorrect password provided"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"Password Error: {self.message}"


class InvalidAmountError(Exception):
    """Exception raised when amount validation fails"""
    def __init__(self, message="Invalid amount provided"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"Amount Error: {self.message}"
    
    def get_error_type(self):
        return "AMOUNT_VALIDATION_ERROR"


class ContractValueError(Exception):
    """Exception raised when contract operation fails"""
    def __init__(self, message="Contract operation failed"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"Contract Error: {self.message}"
    
    def is_contract_related(self):
        return True