"""
Custom exceptions for the Pizza Delivery API
"""
from typing import Dict, Any, Optional

class PizzaDeliveryError(Exception):
    """Base exception for Pizza Delivery API"""
    
    def __init__(self, message: str, code: str = None, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

class ValidationError(PizzaDeliveryError):
    """Raised when input validation fails"""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "VALIDATION_ERROR", details)

class BusinessRuleError(PizzaDeliveryError):
    """Raised when business rules are violated"""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "BUSINESS_RULE_ERROR", details)

class ResourceNotFoundError(PizzaDeliveryError):
    """Raised when a requested resource is not found"""
    
    def __init__(self, resource_type: str, resource_id: Any, details: Dict[str, Any] = None):
        message = f"{resource_type} with ID {resource_id} not found"
        super().__init__(message, "RESOURCE_NOT_FOUND", details)

class DatabaseError(PizzaDeliveryError):
    """Raised when database operations fail"""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "DATABASE_ERROR", details)

def handle_api_error(error: Exception) -> tuple:
    """
    Convert exceptions to API responses
    
    Args:
        error: Exception instance
        
    Returns:
        Tuple of (response_dict, status_code)
    """
    if isinstance(error, ValidationError):
        return {
            'error': error.message,
            'code': error.code,
            'details': error.details
        }, 400
    
    elif isinstance(error, BusinessRuleError):
        return {
            'error': error.message,
            'code': error.code,
            'details': error.details
        }, 400
    
    elif isinstance(error, ResourceNotFoundError):
        return {
            'error': error.message,
            'code': error.code
        }, 404
    
    elif isinstance(error, DatabaseError):
        return {
            'error': 'Database operation failed',
            'code': 'DATABASE_ERROR'
        }, 500
    
    else:
        # Generic error for unexpected exceptions
        return {
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR'
        }, 500
