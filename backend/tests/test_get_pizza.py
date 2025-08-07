from tests.factories.pizza_factory import PizzaFactory

def test_get_pizzas(client):
    pizza = PizzaFactory()

    response = client.get('/api/pizzas/')
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == pizza.name
    assert data[0]['price'] == pizza.price
