import factory
from app.models import Orders
from app.database import db

class OrderFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Orders
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    customer_name = factory.Faker('name')
    phone_number = factory.Sequence(lambda n: f"+1{555:03d}{n:07d}")  # +15550000001, +15550000002, etc.
    total_price = 0.0

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        """Add items to the order if specified"""
        if not create:
            return
        
        if extracted:
            for item in extracted:
                self.items.append(item)
