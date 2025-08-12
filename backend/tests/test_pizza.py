import pytest
from tests.factories.pizza_factory import PizzaFactory
from app.models import Pizza
from app.database import db

class TestPizza:
    def test_pizza_creation(self, session):
        """Test creating a pizza with valid data"""
        pizza = PizzaFactory()
        assert pizza.id is not None
        assert pizza.name.startswith("Test Pizza")
        assert pizza.ingredients == "Cheese, Tomato"
        assert pizza.price == 9.99
        assert pizza.image == "images/test_pizza.jpg"

    def test_pizza_to_dict(self, session):
        """Test pizza serialization to dictionary"""
        pizza = PizzaFactory()
        pizza_dict = pizza.to_dict()
        
        assert pizza_dict['id'] == pizza.id
        assert pizza_dict['name'] == pizza.name
        assert pizza_dict['ingredients'] == pizza.ingredients
        assert pizza_dict['price'] == pizza.price
        assert pizza_dict['image'] == pizza.image

    def test_pizza_validation(self, session):
        """Test pizza model validation"""
        # Test required fields
        pizza = Pizza()
        with pytest.raises(Exception):
            db.session.add(pizza)
            db.session.commit()

    def test_get_pizzas_api(self, client, session):
        """Test GET /api/pizzas/ endpoint"""
        # Create test pizzas
        pizza1 = PizzaFactory(name="Margherita", price=12.99)
        pizza2 = PizzaFactory(name="Pepperoni", price=14.99)
        
        response = client.get('/api/pizzas/')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data) == 2
        
        # Check first pizza
        assert data[0]['name'] == "Margherita"
        assert data[0]['price'] == 12.99
        assert data[0]['ingredients'] == "Cheese, Tomato"
        
        # Check second pizza
        assert data[1]['name'] == "Pepperoni"
        assert data[1]['price'] == 14.99

    def test_pizza_factory_sequence(self, session):
        """Test that pizza factory creates unique names"""
        pizza1 = PizzaFactory()
        pizza2 = PizzaFactory()
        pizza3 = PizzaFactory()
        
        assert pizza1.name != pizza2.name
        assert pizza2.name != pizza3.name
        assert pizza1.name != pizza3.name
