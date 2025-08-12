"""
Order routes for the Pizza Delivery API
"""
from flask import Blueprint, request, jsonify, current_app
from werkzeug.exceptions import BadRequest
from ..services.order_service import OrderService
from ..exceptions import handle_api_error, ValidationError, BusinessRuleError, ResourceNotFoundError
from ..database import db
from marshmallow import ValidationError as MarshmallowValidationError
import logging

# Configure logging
logger = logging.getLogger(__name__)

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/', methods=['POST'])
def create_order():
    """
    Create a new order
    
    ---
    tags:
      - Orders
    summary: Create a new order
    description: Create a new order with customer information and pizza items
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - customer_name
              - phone_number
              - items
            properties:
              customer_name:
                type: string
                minLength: 1
                maxLength: 100
                example: "John Doe"
              phone_number:
                type: string
                pattern: '^\+?1?\d{9,15}$'
                example: "+1234567890"
              items:
                type: array
                minItems: 1
                maxItems: 20
                items:
                  type: object
                  required:
                    - pizza_id
                    - quantity
                  properties:
                    pizza_id:
                      type: integer
                      minimum: 1
                      example: 1
                    quantity:
                      type: integer
                      minimum: 1
                      maximum: 50
                      example: 2
    responses:
      201:
        description: Order created successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Order'
      400:
        description: Validation error or business rule violation
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    try:
        # Check if request is JSON
        if not request.is_json:
            raise ValidationError("Request must be JSON")
        
        # Get request data
        data = request.get_json()
        if not data:
            raise ValidationError("Request body cannot be empty")
        
        # Create service instance
        order_service = OrderService(db.session)
        
        # Create order through service layer
        order = order_service.create_order(data)
        
        # Log successful order creation
        logger.info(f"Order created successfully: ID={order.id}, Customer={order.customer_name}")
        
        return jsonify(order.to_dict()), 201
        
    except BadRequest as e:
        logger.warning(f"Bad request error: {str(e)}")
        return jsonify({
            'error': str(e),
            'code': 'BAD_REQUEST'
        }), 400
        
    except MarshmallowValidationError as e:
        logger.warning(f"Validation error in order creation: {e.messages}")
        return jsonify({
            'error': 'Validation failed',
            'code': 'VALIDATION_ERROR',
            'details': e.messages
        }), 400
        
    except (ValidationError, BusinessRuleError, ValueError) as e:
        logger.warning(f"Business validation error: {str(e)}")
        return jsonify({
            'error': str(e),
            'code': 'VALIDATION_ERROR'
        }), 400
        
    except Exception as e:
        logger.error(f"Unexpected error in order creation: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR'
        }), 500

@order_bp.route('/', methods=['GET'])
def get_orders():
    """
    Get all orders
    
    ---
    tags:
      - Orders
    summary: Retrieve all orders
    description: Get a list of all orders in the system
    responses:
      200:
        description: Orders retrieved successfully
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Order'
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    try:
        # Create service instance
        order_service = OrderService(db.session)
        
        # Get orders through service layer
        orders = order_service.get_all_orders()
        
        # Log successful retrieval
        logger.info(f"Retrieved {len(orders)} orders")
        
        return jsonify([order.to_dict() for order in orders]), 200
        
    except Exception as e:
        logger.error(f"Error retrieving orders: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Failed to retrieve orders',
            'code': 'INTERNAL_ERROR'
        }), 500

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """
    Get order by ID
    
    ---
    tags:
      - Orders
    summary: Retrieve a specific order
    description: Get order details by order ID
    parameters:
      - name: order_id
        in: path
        required: true
        schema:
          type: integer
          minimum: 1
        example: 1
    responses:
      200:
        description: Order retrieved successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Order'
      404:
        description: Order not found
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    try:
        # Create service instance
        order_service = OrderService(db.session)
        
        # Get order through service layer
        order = order_service.get_order_by_id(order_id)
        
        if not order:
            raise ResourceNotFoundError("Order", order_id)
        
        # Log successful retrieval
        logger.info(f"Retrieved order: ID={order_id}")
        
        return jsonify(order.to_dict()), 200
        
    except ResourceNotFoundError as e:
        logger.info(f"Order not found: ID={order_id}")
        return jsonify({
            'error': str(e),
            'code': e.code
        }), 404
        
    except Exception as e:
        logger.error(f"Error retrieving order {order_id}: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Failed to retrieve order',
            'code': 'INTERNAL_ERROR'
        }), 500
