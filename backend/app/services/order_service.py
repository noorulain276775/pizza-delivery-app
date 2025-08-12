"""
Order service layer for business logic
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from ..models import Orders, OrderItem, Pizza
from ..schemas import validate_order_data
from marshmallow import ValidationError
from decimal import Decimal

class OrderService:
    """Service class for order operations"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create_order(self, order_data: Dict[str, Any]) -> Orders:
        """
        Create a new order with validation and business logic
        
        Args:
            order_data: Validated order data
            
        Returns:
            Created order instance
            
        Raises:
            ValidationError: If data validation fails
            ValueError: If business rules are violated
        """
        try:
            # Validate input data
            validated_data = validate_order_data(order_data)
            
            # Business logic validation
            self._validate_business_rules(validated_data)
            
            # Create order
            order = Orders(
                customer_name=validated_data['customer_name'],
                phone_number=validated_data['phone_number'],
                total_price=Decimal('0.00')
            )
            
            self.db.add(order)
            self.db.flush()  # Get the order ID
            
            # Process order items
            total_price = self._process_order_items(order, validated_data['items'])
            
            # Update order total
            order.total_price = total_price
            
            # Commit transaction
            self.db.commit()
            
            return order
            
        except ValidationError:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to create order: {str(e)}")
    
    def get_all_orders(self) -> List[Orders]:
        """Get all orders"""
        try:
            return self.db.query(Orders).order_by(Orders.created_at.desc()).all()
        except Exception as e:
            raise ValueError(f"Failed to retrieve orders: {str(e)}")
    
    def get_order_by_id(self, order_id: int) -> Optional[Orders]:
        """Get order by ID"""
        try:
            return self.db.get(Orders, order_id)
        except Exception as e:
            raise ValueError(f"Failed to retrieve order: {str(e)}")
    
    def _validate_business_rules(self, data: Dict[str, Any]) -> None:
        """
        Validate business rules
        
        Args:
            data: Validated order data
            
        Raises:
            ValueError: If business rules are violated
        """
        # Check if pizzas exist
        pizza_ids = [item['pizza_id'] for item in data['items']]
        existing_pizzas = self.db.query(Pizza).filter(Pizza.id.in_(pizza_ids)).all()
        existing_pizza_ids = {pizza.id for pizza in existing_pizzas}
        
        missing_pizza_ids = set(pizza_ids) - existing_pizza_ids
        if missing_pizza_ids:
            raise ValueError(f"Pizzas with IDs {missing_pizza_ids} do not exist")
        
        # Check total order value (business rule: max $500 per order)
        total_value = sum(
            next(pizza.price for pizza in existing_pizzas if pizza.id == item['pizza_id']) * item['quantity']
            for item in data['items']
        )
        
        if total_value > 500.0:
            raise ValueError("Order total cannot exceed $500")
    
    def _process_order_items(self, order: Orders, items_data: List[Dict[str, Any]]) -> Decimal:
        """
        Process order items and calculate total
        
        Args:
            order: Order instance
            items_data: List of item data
            
        Returns:
            Total price for the order
        """
        total_price = Decimal('0.00')
        
        for item_data in items_data:
            pizza = self.db.get(Pizza, item_data['pizza_id'])
            
            # Create order item
            order_item = OrderItem(
                order_id=order.id,
                pizza_id=item_data['pizza_id'],
                quantity=item_data['quantity']
            )
            
            self.db.add(order_item)
            
            # Calculate item total
            item_total = Decimal(str(pizza.price)) * item_data['quantity']
            total_price += item_total
        
        return total_price
