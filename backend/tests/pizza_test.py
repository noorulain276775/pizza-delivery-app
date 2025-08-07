from .conftest import client

# def test_create_pizza(client):
#     new_pizza = {
#         "name": "Cheese Burst",
#         "ingredients": "Cheese, Tomato",
#         "price": 8.99,
#         "image": "images/cheese_burst.jpg"
#     }

#     response = client.post("/api/pizzas/", json=new_pizza)
#     assert response.status_code == 201

def test_get_pizzas(client):
    response = client.get('/api/pizzas/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == "Test Pizza"
    assert data[0]['price'] == 5.99
