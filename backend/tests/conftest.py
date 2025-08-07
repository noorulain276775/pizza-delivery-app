import pytest
from config import TestConfig
from app import create_app
from app.models import Pizza
from app.database import db


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        test_pizza = Pizza(name="Test Pizza", ingredients="Test Ingredients", price=5.99, image="images/test_pizza.jpg")
        db.session.add(test_pizza)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
