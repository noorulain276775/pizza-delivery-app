import pytest
import json
from tests.factories.pizza_factory import PizzaFactory
from tests.factories.order_factory import OrderFactory
from tests.factories.order_item_factory import OrderItemFactory
from app.models import Orders, OrderItem, Pizza
from app.database import db

class TestGetOrdersAPI:
    def test_get_orders_empty(self, client, session):
        """Test getting orders when database is empty"""
        response = client.get('/api/orders/')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert data == []

    def test_get_orders_with_data(self, client, session):
        """Test getting orders with existing data"""
        # Create test pizzas
        pizza1 = PizzaFactory(name="Margherita", price=12.99)
        pizza2 = PizzaFactory(name="Pepperoni", price=15.99)
        
        # Create test orders
        order1 = OrderFactory(customer_name="John Doe")
        order2 = OrderFactory(customer_name="Jane Smith")
        
        # Add items to orders
        OrderItemFactory(pizza=pizza1, order_id=order1.id, quantity=2)
        OrderItemFactory(pizza=pizza2, order_id=order2.id, quantity=1)
        
        response = client.get('/api/orders/')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data) == 2
        
        # Check that orders are returned (order may vary due to factory sequence)
        customer_names = [order['customer_name'] for order in data]
        assert "John Doe" in customer_names
        assert "Jane Smith" in customer_names

    def test_get_order_by_id_success(self, client, session):
        """Test getting a specific order by ID"""
        # Create test pizza and order
        pizza = PizzaFactory(name="Margherita", price=12.99)
        order = OrderFactory(customer_name="Bob Wilson")
        
        # Add item to order
        OrderItemFactory(pizza=pizza, order_id=order.id, quantity=2)
        
        response = client.get(f'/api/orders/{order.id}')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['id'] == order.id
        assert data['customer_name'] == "Bob Wilson"
        assert data['total_price'] == round(12.99 * 2, 2)

    def test_get_order_by_id_not_found(self, client, session):
        """Test getting order with non-existent ID"""
        response = client.get('/api/orders/999')
        
        assert response.status_code == 404
        
        data = response.get_json()
        assert 'Order with ID 999 not found' in data['error']

    def test_get_order_with_multiple_items(self, client, session):
        """Test getting order with multiple items"""
        # Create test pizzas
        pizza1 = PizzaFactory(name="Margherita", price=12.99)
        pizza2 = PizzaFactory(name="Pepperoni", price=15.99)
        
        # Create order
        order = OrderFactory(customer_name="Alice Johnson")
        
        # Add multiple items
        OrderItemFactory(pizza=pizza1, order_id=order.id, quantity=2)
        OrderItemFactory(pizza=pizza2, order_id=order.id, quantity=1)
        
        response = client.get(f'/api/orders/{order.id}')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['id'] == order.id
        assert len(data['items']) == 2
        
        # Check total price
        expected_total = round(12.99 * 2 + 15.99 * 1, 2)
        assert data['total_price'] == expected_total

    def test_get_orders_serialization(self, client, session):
        """Test that orders are properly serialized"""
        # Create test order
        order = OrderFactory()
        
        response = client.get('/api/orders/')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data) == 1
        
        order_data = data[0]
        required_fields = ['id', 'customer_name', 'phone_number', 'total_price', 'created_at', 'updated_at', 'items']
        
        for field in required_fields:
            assert field in order_data
