# Pizza Delivery App API Documentation

## Overview
This is the backend API for a Pizza Delivery application built with Flask, SQLAlchemy, and SQLite.

## Base URL
```
http://localhost:5000
```

## API Endpoints

### 1. Pizza Management

#### GET /api/pizzas/
Retrieve all available pizzas.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Margherita",
    "ingredients": "Fresh mozzarella, tomato sauce, fresh basil",
    "price": 12.99,
    "image": "images/margherita.jpg"
  }
]
```

**Status Codes:**
- `200 OK` - Successfully retrieved pizzas

---

### 2. Order Management

#### POST /api/orders/
Create a new order.

**Request Body:**
```json
{
  "customer_name": "John Doe",
  "phone_number": "+1234567890",
  "items": [
    {
      "pizza_id": 1,
      "quantity": 2
    },
    {
      "pizza_id": 2,
      "quantity": 1
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "customer_name": "John Doe",
  "phone_number": "+1234567890",
  "total_price": 41.97,
  "created_at": "2025-08-12T12:43:01",
  "items": [
    {
      "id": 1,
      "order_id": 1,
      "pizza_id": 1,
      "pizza_name": "Margherita",
      "quantity": 2
    },
    {
      "id": 2,
      "order_id": 1,
      "pizza_id": 2,
      "pizza_name": "Pepperoni",
      "quantity": 1
    }
  ]
}
```

**Status Codes:**
- `201 Created` - Order successfully created
- `400 Bad Request` - Invalid input data
- `500 Internal Server Error` - Server error

**Validation Rules:**
- `customer_name` is required
- `phone_number` is required
- `items` must be a non-empty list
- Each item must have `pizza_id` and `quantity`
- `quantity` must be greater than 0
- `pizza_id` must reference an existing pizza

---

#### GET /api/orders/
Retrieve all orders.

**Response:**
```json
[
  {
    "id": 1,
    "customer_name": "John Doe",
    "phone_number": "+1234567890",
    "total_price": 41.97,
    "created_at": "2025-08-12T12:43:01",
    "items": [...]
  }
]
```

**Status Codes:**
- `200 OK` - Successfully retrieved orders

---

#### GET /api/orders/{order_id}
Retrieve a specific order by ID.

**Response:**
```json
{
  "id": 1,
  "customer_name": "John Doe",
  "phone_number": "+1234567890",
  "total_price": 41.97,
  "created_at": "2025-08-12T12:43:01",
  "items": [...]
}
```

**Status Codes:**
- `200 OK` - Successfully retrieved order
- `404 Not Found` - Order not found

---

## Data Models

### Pizza
- `id` (Integer, Primary Key)
- `name` (String, Required)
- `ingredients` (String, Required)
- `price` (Float, Required)
- `image` (String, Required)

### Order
- `id` (Integer, Primary Key)
- `customer_name` (String, Required)
- `phone_number` (String, Required)
- `total_price` (Float, Required)
- `created_at` (DateTime, Auto-generated)

### OrderItem
- `id` (Integer, Primary Key)
- `order_id` (Integer, Foreign Key to Order)
- `pizza_id` (Integer, Foreign Key to Pizza)
- `quantity` (Integer, Required)

## Error Handling

All API endpoints return consistent error responses:

```json
{
  "error": "Error message description"
}
```

## Testing

The application includes comprehensive test coverage:

- **38 test cases** covering all API endpoints
- **Test factories** for generating test data
- **Isolated test database** for each test
- **Coverage includes:**
  - Order creation with validation
  - Order retrieval (all and by ID)
  - Pizza listing
  - Model validation
  - Error handling
  - Edge cases

## Setup and Running

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Tests
```bash
cd backend
python -m pytest tests/ -v
```

### 3. Seed Database
```bash
cd backend
python seed_data.py
```

### 4. Run Application
```bash
cd backend
python run.py
```

## Database

- **SQLite** database with SQLAlchemy ORM
- **Alembic** for database migrations
- **Automatic total price calculation** for orders
- **Proper foreign key relationships** between orders, items, and pizzas

## Security Features

- **Input validation** for all user inputs
- **SQL injection protection** via SQLAlchemy ORM
- **CORS enabled** for frontend integration
- **Error handling** without exposing internal details

## Future Enhancements

Potential additional endpoints that could be added:
- **PUT /api/orders/{order_id}** - Update order status
- **DELETE /api/orders/{order_id}** - Cancel order
- **POST /api/pizzas/** - Add new pizza (admin)
- **PUT /api/pizzas/{pizza_id}** - Update pizza (admin)
- **DELETE /api/pizzas/{pizza_id}** - Remove pizza (admin)
- **GET /api/orders?status=pending** - Filter orders by status
- **Authentication and authorization** for admin operations
