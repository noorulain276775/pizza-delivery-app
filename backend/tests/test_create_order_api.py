import pytest
import json
from tests.factories.pizza_factory import PizzaFactory
from tests.factories.order_factory import OrderFactory
from tests.factories.order_item_factory import OrderItemFactory
from app.models import Orders, OrderItem, Pizza
from app.database import db

class TestCreateOrderAPI:
    def test_create_order_success(self, client, session):
        """Test successful order creation with valid data"""
        # Create test pizzas
        pizza1 = PizzaFactory(name="Margherita", price=12.99)
        pizza2 = PizzaFactory(name="Pepperoni", price=15.99)
        
        order_data = {
            "customer_name": "John Doe",
            "phone_number": "+15551234567",
            "items": [
                {"pizza_id": pizza1.id, "quantity": 2},
                {"pizza_id": pizza2.id, "quantity": 1}
            ]
        }
        
        response = client.post(
            '/api/orders/',
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        
        data = response.get_json()
        assert data['customer_name'] == "John Doe"
        assert data['phone_number'] == "+15551234567"
        assert data['total_price'] == round(12.99 * 2 + 15.99 * 1, 2)
        
        # Check items count using .count() method
        order = db.session.get(Orders, data['id'])
        assert order.items.count() == 2

    def test_create_order_missing_required_fields(self, client, session):
        """Test order creation with missing required fields"""
        order_data = {
            "phone_number": "+15551234567",
            "items": [{"pizza_id": 1, "quantity": 2}]
        }
        
        response = client.post(
            '/api/orders/',
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'Validation failed' in data['error']
        assert 'customer_name' in str(data['details'])

    def test_create_order_empty_items(self, client, session):
        """Test order creation with empty items list"""
        order_data = {
            "customer_name": "John Doe",
            "phone_number": "+15551234567",
            "items": []
        }
        
        response = client.post(
            '/api/orders/',
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'Validation failed' in data['error']
        assert 'items' in str(data['details'])

    def test_create_order_invalid_pizza_id(self, client, session):
        """Test order creation with non-existent pizza ID"""
        order_data = {
            "customer_name": "John Doe",
            "phone_number": "+15551234567",
            "items": [{"pizza_id": 999, "quantity": 2}]
        }
        
        response = client.post(
            '/api/orders/',
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'Pizzas with IDs {999} do not exist' in data['error']

    def test_create_order_invalid_quantity(self, client, session):
        """Test order creation with invalid quantity"""
        pizza = PizzaFactory(name="Margherita", price=12.99)
        
        order_data = {
            "customer_name": "John Doe",
            "phone_number": "+15551234567",
            "items": [{"pizza_id": pizza.id, "quantity": 0}]
        }
        
        response = client.post(
            '/api/orders/',
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'Validation failed' in data['error']
        assert 'quantity' in str(data['details'])

    def test_create_order_calculates_total_correctly(self, client, session):
        """Test order total price calculation"""
        pizza = PizzaFactory(name="Margherita", price=12.99)
        
        order_data = {
            "customer_name": "John Doe",
            "phone_number": "+15551234567",
            "items": [{"pizza_id": pizza.id, "quantity": 3}]
        }
        
        response = client.post(
            '/api/orders/',
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        
        data = response.get_json()
        expected_total = round(12.99 * 3, 2)
        assert data['total_price'] == expected_total

    def test_create_order_with_single_item(self, client, session):
        """Test order creation with single item"""
        pizza = PizzaFactory(name="Margherita", price=12.99)
        
        order_data = {
            "customer_name": "John Doe",
            "phone_number": "+15551234567",
            "items": [{"pizza_id": pizza.id, "quantity": 1}]
        }
        
        response = client.post(
            '/api/orders/',
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        
        data = response.get_json()
        assert data['total_price'] == 12.99
        assert data['items'][0]['quantity'] == 1

    def test_create_order_invalid_json(self, client, session):
        """Test order creation with invalid JSON"""
        response = client.post(
            '/api/orders/',
            data="invalid json",
            content_type='application/json'
        )
        
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'Bad Request' in data['error']
        assert 'browser (or proxy) sent a request that this server could not understand' in data['error']
