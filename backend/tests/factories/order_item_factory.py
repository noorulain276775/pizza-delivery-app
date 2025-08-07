import factory
from app.models import OrderItem, Pizza
from app.database import db

class OrderItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = OrderItem
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    pizza = factory.SubFactory('tests.factories.pizza_factory.PizzaFactory')
    quantity = 1
    order_id = None  # Will be set when attached to an Order
    pizza_id = factory.SelfAttribute('pizza.id')
