import pytest
import json
from tests.factories.pizza_factory import PizzaFactory
from tests.factories.order_factory import OrderFactory
from tests.factories.order_item_factory import OrderItemFactory
from app.models import Orders, OrderItem, Pizza
from app.database import db

class TestOrders:
    def test_order_creation(self, session):
        """Test creating an order with valid data"""
        order = OrderFactory()
        assert order.id is not None
        assert order.customer_name is not None
        assert order.phone_number is not None
        assert order.total_price == 0.0

    def test_order_to_dict(self, session):
        """Test order serialization to dictionary"""
        order = OrderFactory()
        order_dict = order.to_dict()
        
        assert order_dict['id'] == order.id
        assert order_dict['customer_name'] == order.customer_name
        assert order_dict['phone_number'] == order.phone_number
        assert order_dict['total_price'] == float(order.total_price)
        assert order_dict['created_at'] is not None
        assert order_dict['updated_at'] is not None
        assert 'items' in order_dict

    def test_order_with_items(self, session):
        """Test order with multiple items"""
        # Create pizzas
        pizza1 = PizzaFactory(price=12.99)
        pizza2 = PizzaFactory(price=15.99)
        
        # Create order
        order = OrderFactory()
        
        # Create order items
        OrderItemFactory(pizza=pizza1, order_id=order.id, quantity=2)
        OrderItemFactory(pizza=pizza2, order_id=order.id, quantity=1)
        
        # Refresh order
        db.session.refresh(order)
        
        # Check items count
        assert order.items.count() == 2
        
        # Check total price
        expected_total = round(12.99 * 2 + 15.99 * 1, 2)
        assert float(order.total_price) == expected_total

    def test_order_validation(self, session):
        """Test order validation rules"""
        # Test valid order
        order = OrderFactory()
        assert order.customer_name is not None
        assert order.phone_number is not None
        
        # Test phone number format
        assert order.phone_number.startswith('+1')
        assert len(order.phone_number) == 12  # +1 + 10 digits

    def test_order_factory_post_generation(self, session):
        """Test order factory post-generation hook"""
        pizza = PizzaFactory(price=10.00)
        order = OrderFactory()
        
        # Create order item
        OrderItemFactory(pizza=pizza, order_id=order.id, quantity=2)
        
        # Refresh order
        db.session.refresh(order)
        
        # Check total price
        expected_total = 20.00
        assert float(order.total_price) == expected_total

    def test_order_relationships(self, session):
        """Test order relationships with order items"""
        order = OrderFactory()
        pizza = PizzaFactory()
        
        # Create order item
        item = OrderItemFactory(pizza=pizza, order_id=order.id, quantity=2)
        
        # Refresh order
        db.session.refresh(order)
        
        # Check relationships
        assert order.items.count() == 1
        assert item.order_id == order.id
        assert item.pizza_id == pizza.id

    def test_order_total_price_calculation(self, session):
        """Test order total price calculation with multiple items"""
        order = OrderFactory()
        
        # Create multiple pizzas with different prices
        pizza1 = PizzaFactory(price=12.99)
        pizza2 = PizzaFactory(price=18.50)
        pizza3 = PizzaFactory(price=9.99)
        
        # Create order items
        OrderItemFactory(pizza=pizza1, order_id=order.id, quantity=1)
        OrderItemFactory(pizza=pizza2, order_id=order.id, quantity=2)
        OrderItemFactory(pizza=pizza3, order_id=order.id, quantity=3)
        
        # Refresh order
        db.session.refresh(order)
        
        expected_total = round(12.99 + (18.50 * 2) + (9.99 * 3), 2)
        assert float(order.total_price) == expected_total
