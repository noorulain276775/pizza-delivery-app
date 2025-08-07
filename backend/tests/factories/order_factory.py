import factory
from app.models import Orders
from app.database import db
from datetime import datetime

class OrderFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Orders
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    customer_name = factory.Faker('name')
    phone_number = factory.Faker('phone_number')
    total_price = 0.0  # We'll calculate this after items are attached
    created_at = factory.LazyFunction(datetime.utcnow)

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for item in extracted:
                self.items.append(item)
            self.total_price = sum(item.calculated_item_total for item in self.items)
            db.session.commit()
