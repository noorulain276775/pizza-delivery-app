"""
Validation schemas for the Pizza Delivery API
"""
from marshmallow import Schema, fields, validate, ValidationError
from typing import Dict, Any

class OrderItemSchema(Schema):
    """Schema for order item validation"""
    pizza_id = fields.Integer(required=True, validate=validate.Range(min=1))
    quantity = fields.Integer(required=True, validate=validate.Range(min=1, max=50))

class CreateOrderSchema(Schema):
    """Schema for order creation validation"""
    customer_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100),
        error_messages={
            'required': 'Customer name is required',
            'invalid': 'Customer name must be a valid string',
            'validator_failed': 'Customer name must be between 1 and 100 characters'
        }
    )
    phone_number = fields.Str(
        required=True,
        validate=validate.Regexp(
            r'^\+?1?\d{9,15}$',
            error='Phone number must be a valid international format (e.g., +1234567890)'
        ),
        error_messages={
            'required': 'Phone number is required',
            'invalid': 'Phone number must be a valid string'
        }
    )
    items = fields.List(
        fields.Nested(OrderItemSchema),
        required=True,
        validate=validate.Length(min=1, max=20),
        error_messages={
            'required': 'Order items are required',
            'invalid': 'Items must be a list',
            'validator_failed': 'Order must have between 1 and 20 items'
        }
    )

class OrderItemResponseSchema(Schema):
    """Schema for order item response serialization"""
    id = fields.Integer()
    order_id = fields.Integer()
    pizza_id = fields.Integer()
    pizza_name = fields.Str()
    quantity = fields.Integer()
    calculated_item_total = fields.Float()

class OrderResponseSchema(Schema):
    """Schema for order response serialization"""
    id = fields.Integer()
    customer_name = fields.Str()
    phone_number = fields.Str()
    total_price = fields.Float()
    created_at = fields.DateTime()
    items = fields.List(fields.Nested(OrderItemResponseSchema))

class PizzaResponseSchema(Schema):
    """Schema for pizza response serialization"""
    id = fields.Integer()
    name = fields.Str()
    ingredients = fields.Str()
    price = fields.Float()
    image = fields.Str()

class ErrorResponseSchema(Schema):
    """Schema for error response serialization"""
    error = fields.Str(required=True)
    code = fields.Str()
    details = fields.Dict()

def validate_order_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate order data using the schema
    
    Args:
        data: Raw order data from request
        
    Returns:
        Validated and cleaned data
        
    Raises:
        ValidationError: If validation fails
    """
    schema = CreateOrderSchema()
    try:
        validated_data = schema.load(data)
        return validated_data
    except ValidationError as e:
        # Convert marshmallow errors to user-friendly format
        error_messages = []
        for field, errors in e.messages.items():
            if isinstance(errors, list):
                error_messages.extend([f"{field}: {error}" for error in errors])
            else:
                error_messages.append(f"{field}: {errors}")
        
        raise ValidationError(
            f"Validation failed: {'; '.join(error_messages)}"
        )
