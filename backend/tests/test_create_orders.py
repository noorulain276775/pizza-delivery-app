import pytest
import json
from tests.factories.pizza_factory import PizzaFactory
from tests.factories.order_factory import OrderFactory
from tests.factories.order_item_factory import OrderItemFactory
from app.models import Orders, OrderItem, Pizza
from app.database import db

def test_create_orders(client, session):
    """Test creating multiple orders"""
    # Create test pizzas
    pizza1 = PizzaFactory(name="Margherita", price=12.99)
    pizza2 = PizzaFactory(name="Pepperoni", price=15.99)
    
    # Create first order
    order_data1 = {
        "customer_name": "John Doe",
        "phone_number": "+1234567890",
        "items": [{"pizza_id": pizza1.id, "quantity": 2}]
    }
    
    response1 = client.post(
        '/api/orders/',
        data=json.dumps(order_data1),
        content_type='application/json'
    )
    
    assert response1.status_code == 201
    data1 = response1.get_json()
    assert data1['customer_name'] == "John Doe"
    assert data1['total_price'] == 25.98  # 12.99 * 2
    
    # Create second order
    order_data2 = {
        "customer_name": "Jane Smith",
        "phone_number": "+0987654321",
        "items": [{"pizza_id": pizza2.id, "quantity": 1}]
    }
    
    response2 = client.post(
        '/api/orders/',
        data=json.dumps(order_data2),
        content_type='application/json'
    )
    
    assert response2.status_code == 201
    data2 = response2.get_json()
    assert data2['customer_name'] == "Jane Smith"
    assert data2['total_price'] == 15.99
    
    # Verify orders were saved to database
    saved_order = db.session.get(Orders, data1["id"])
    assert saved_order is not None
    assert saved_order.customer_name == "John Doe"
