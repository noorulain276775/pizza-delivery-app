import pytest
from tests.factories.pizza_factory import PizzaFactory
from app.models import Pizza
from app.database import db

class TestPizzaAPI:
    def test_get_pizzas_empty(self, client, session):
        """Test getting pizzas when none exist"""
        response = client.get('/api/pizzas/')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data == []

    def test_get_pizzas_with_data(self, client, session):
        """Test getting all pizzas"""
        # Create test pizzas
        pizza1 = PizzaFactory(name="Margherita", price=12.99, ingredients="Mozzarella, Tomato, Basil")
        pizza2 = PizzaFactory(name="Pepperoni", price=15.99, ingredients="Mozzarella, Pepperoni, Tomato")
        
        response = client.get('/api/pizzas/')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data) == 2
        
        # Check first pizza
        assert data[0]['name'] == "Margherita"
        assert data[0]['price'] == 12.99
        assert data[0]['ingredients'] == "Mozzarella, Tomato, Basil"
        
        # Check second pizza
        assert data[1]['name'] == "Pepperoni"
        assert data[1]['price'] == 15.99
        assert data[1]['ingredients'] == "Mozzarella, Pepperoni, Tomato"

    def test_pizza_data_structure(self, client, session):
        """Test that pizza data structure is correct"""
        pizza = PizzaFactory(
            name="Test Pizza",
            price=20.00,
            ingredients="Test Ingredients",
            image="test_image.jpg"
        )
        
        response = client.get('/api/pizzas/')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data) == 1
        
        pizza_data = data[0]
        required_fields = ['id', 'name', 'ingredients', 'price', 'image']
        for field in required_fields:
            assert field in pizza_data
        
        assert pizza_data['name'] == "Test Pizza"
        assert pizza_data['price'] == 20.00
        assert pizza_data['ingredients'] == "Test Ingredients"
        assert pizza_data['image'] == "test_image.jpg"

    def test_pizza_factory_creates_unique_pizzas(self, client, session):
        """Test that pizza factory creates unique pizzas"""
        # Create multiple pizzas
        PizzaFactory()
        PizzaFactory()
        PizzaFactory()
        
        response = client.get('/api/pizzas/')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data) == 3
        
        # Check that all pizzas have unique IDs
        pizza_ids = [pizza['id'] for pizza in data]
        assert len(pizza_ids) == len(set(pizza_ids))
        
        # Check that names are different (factory uses sequence)
        pizza_names = [pizza['name'] for pizza in data]
        assert len(pizza_names) == len(set(pizza_names))
