from tests.factories.pizza_factory import PizzaFactory
from app.models import Orders
from app.database import db

def test_create_orders(client, app):
    with app.app_context():
        margherita = PizzaFactory(name="Margherita", price=10.0)
        pepperoni = PizzaFactory(name="Pepperoni", price=12.5)
        db.session.commit()

        order_payload = {
            "customer_name": "Noor ul Ain",
            "phone_number": "+358400000000",
            "items": [
                {"pizza_id": margherita.id, "quantity": 2},
                {"pizza_id": pepperoni.id, "quantity": 1},
            ]
        }

        response = client.post('/api/orders/', json=order_payload)
        assert response.status_code == 201

        data = response.get_json()
        assert data["customer_name"] == "Noor ul Ain"
        assert data["phone_number"] == "+358400000000"
        assert len(data["items"]) == 2

        expected_total = 2 * margherita.price + 1 * pepperoni.price
        assert data["total_price"] == expected_total

        saved_order = Orders.query.get(data["id"])
        assert saved_order is not None
        assert saved_order.total_price == expected_total
        assert len(saved_order.items) == 2
