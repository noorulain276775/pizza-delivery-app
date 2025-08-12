"""
Pizza routes for the Pizza Delivery API
"""
from flask import Blueprint, jsonify, current_app
from ..services.pizza_service import PizzaService
from ..exceptions import ResourceNotFoundError
from ..database import db
import logging

# Configure logging
logger = logging.getLogger(__name__)

pizza_bp = Blueprint('pizza_bp', __name__)

@pizza_bp.route('/', methods=['GET'])
def get_pizzas():
    """
    Get all pizzas
    
    ---
    tags:
      - Pizzas
    summary: Retrieve all available pizzas
    description: Get a list of all pizzas available for ordering
    responses:
      200:
        description: Pizzas retrieved successfully
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Pizza'
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
    """
    try:
        # Create service instance
        pizza_service = PizzaService(db.session)
        
        # Get pizzas through service layer
        pizzas = pizza_service.get_all_pizzas()
        
        # Log successful retrieval
        logger.info(f"Retrieved {len(pizzas)} pizzas")
        
        return jsonify([pizza.to_dict() for pizza in pizzas]), 200
        
    except Exception as e:
        logger.error(f"Error retrieving pizzas: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Failed to retrieve pizzas',
            'code': 'INTERNAL_ERROR'
        }), 500

@pizza_bp.route('/<int:pizza_id>', methods=['GET'])
def get_pizza(pizza_id):
    """
    Get pizza by ID
    
    ---
    tags:
      - Pizzas
    summary: Retrieve a specific pizza
    description: Get pizza details by pizza ID
    parameters:
      - name: pizza_id
        in: path
        required: true
        schema:
          type: integer
          minimum: 1
        example: 1
    responses:
      200:
        description: Pizza retrieved successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Pizza'
      404:
        description: Pizza not found
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
        pizza_service = PizzaService(db.session)
        
        # Get pizza through service layer
        pizza = pizza_service.get_pizza_by_id(pizza_id)
        
        # Log successful retrieval
        logger.info(f"Retrieved pizza: ID={pizza_id}, Name={pizza.name}")
        
        return jsonify(pizza.to_dict()), 200
        
    except ResourceNotFoundError as e:
        logger.info(f"Pizza not found: ID={pizza_id}")
        return jsonify({
            'error': str(e),
            'code': e.code
        }), 404
        
    except Exception as e:
        logger.error(f"Error retrieving pizza {pizza_id}: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Failed to retrieve pizza',
            'code': 'INTERNAL_ERROR'
        }), 500
