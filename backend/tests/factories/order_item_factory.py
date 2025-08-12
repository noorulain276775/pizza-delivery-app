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

    @factory.post_generation
    def update_order_total(self, create, extracted, **kwargs):
        """Update the order's total price after creating the order item"""
        if create and self.order_id:
            # Get the order and update its total price
            from app.models import Orders
            order = db.session.get(Orders, self.order_id)
            if order:
                order.update_total_price()
                db.session.commit()
