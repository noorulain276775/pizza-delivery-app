import pytest
from tests.factories.pizza_factory import PizzaFactory
from tests.factories.order_factory import OrderFactory
from tests.factories.order_item_factory import OrderItemFactory
from app.models import Orders, OrderItem, Pizza
from app.database import db

class TestOrderItem:
    def test_order_item_creation(self, session):
        """Test creating an order item with valid data"""
        pizza = PizzaFactory(name="Test Pizza")
        order = OrderFactory()
        order_item = OrderItemFactory(pizza=pizza, order_id=order.id, quantity=2)
        
        assert order_item.id is not None
        assert order_item.pizza_id == pizza.id
        assert order_item.order_id == order.id
        assert order_item.quantity == 2

    def test_order_item_to_dict(self, session):
        """Test order item serialization to dictionary"""
        pizza = PizzaFactory(name="Test Pizza")
        order = OrderFactory()
        order_item = OrderItemFactory(pizza=pizza, order_id=order.id, quantity=2)
        
        order_dict = order_item.to_dict()
        
        assert order_dict['id'] == order_item.id
        assert order_dict['order_id'] == order_item.order_id
        assert order_dict['pizza_id'] == order_item.pizza_id
        assert order_dict['pizza_name'] == pizza.name
        assert order_dict['quantity'] == order_item.quantity
        assert 'calculated_item_total' in order_dict

    def test_calculated_item_total(self, session):
        """Test order item total calculation"""
        pizza = PizzaFactory(price=15.99)
        order = OrderFactory()
        order_item = OrderItemFactory(pizza=pizza, order_id=order.id, quantity=2)
        
        expected_total = 15.99 * 2
        assert float(order_item.calculated_item_total) == expected_total

    def test_order_item_relationships(self, session):
        """Test order item relationships with pizza and order"""
        pizza = PizzaFactory()
        order = OrderFactory()
        order_item = OrderItemFactory(pizza=pizza, order_id=order.id, quantity=2)
        
        # Test relationships
        assert order_item.pizza.id == pizza.id
        assert order_item.order.id == order.id
        assert order_item.pizza.name == pizza.name

    def test_order_item_validation(self, session):
        """Test order item validation rules"""
        pizza = PizzaFactory()
        order = OrderFactory()
        
        # Test valid quantity
        order_item = OrderItemFactory(pizza=pizza, order_id=order.id, quantity=1)
        assert order_item.quantity == 1
        
        # Test quantity limits
        with pytest.raises(ValueError):
            OrderItemFactory(pizza=pizza, order_id=order.id, quantity=0)
        
        with pytest.raises(ValueError):
            OrderItemFactory(pizza=pizza, order_id=order.id, quantity=51)

    def test_order_item_factory_defaults(self, session):
        """Test order item factory creates items with correct defaults"""
        pizza = PizzaFactory()
        order = OrderFactory()
        
        order_item = OrderItemFactory(pizza=pizza, order_id=order.id)
        
        assert order_item.quantity == 1
        assert order_item.pizza_id == pizza.id
        assert order_item.order_id == order.id
