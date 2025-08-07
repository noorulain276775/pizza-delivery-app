import factory
from app.models import Pizza
from app.database import db

class PizzaFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Pizza
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    name = factory.Sequence(lambda n: f"Test Pizza {n}")
    ingredients = "Cheese, Tomato"
    price = 9.99
    image = "images/test_pizza.jpg"
