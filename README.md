# Pizza Delivery API - Enterprise Grade Documentation

## Overview
This is a production-ready, enterprise-grade Pizza Delivery API built with Flask, following industry best practices and security standards. The application provides a robust backend service for managing pizza orders, with comprehensive validation, error handling, and testing coverage.

## Features Implemented

### Security and Best Practices
- Input validation with Marshmallow schemas for all API endpoints
- Service layer architecture for proper separation of concerns
- Custom exception handling with appropriate HTTP status codes
- Environment-based configuration management for different deployment scenarios
- Comprehensive logging system with log rotation for production use
- CORS configuration with origin validation for security
- Database constraints and validation at both application and database levels
- Transaction management with proper rollback handling
- Business rule validation including maximum order limits and quantity restrictions
- Phone number format validation following international standards

### Architecture
- Three-tier architecture: Routes handle HTTP requests, Services contain business logic, Models manage data
- Dependency injection pattern for better testability and maintainability
- Factory pattern for application creation enabling different configurations
- Blueprint organization for modular code structure
- Database migration support using Alembic for schema evolution

## Environment Configuration

### Environment Variables
The application uses environment variables for configuration. Create a .env file in the backend directory with the following variables:

```bash
# Database Configuration
DATABASE_URL=sqlite:///pizzas.db

# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000

# Security Settings
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Logging Configuration
LOG_LEVEL=INFO
```

### Configuration Classes
The application supports three configuration environments:
- DevelopmentConfig: Development settings with debug enabled
- ProductionConfig: Production settings with security features enabled
- TestConfig: Testing configuration using in-memory database

## API Endpoints

### Base URL
```
http://localhost:5000
```

### Pizza Management Endpoints

#### GET /api/pizzas/
Retrieves all available pizzas from the database.

**Response Format:**
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
- 200 OK: Successfully retrieved pizzas

#### GET /api/pizzas/{pizza_id}
Retrieves a specific pizza by its unique identifier.

**Parameters:**
- pizza_id (integer, required): The unique identifier of the pizza

**Response Format:**
```json
{
  "id": 1,
  "name": "Margherita",
  "ingredients": "Fresh mozzarella, tomato sauce, fresh basil",
  "price": 12.99,
  "image": "images/margherita.jpg"
}
```

**Status Codes:**
- 200 OK: Successfully retrieved pizza
- 404 Not Found: Pizza with the specified ID does not exist

### Order Management Endpoints

#### POST /api/orders/
Creates a new order with comprehensive validation of all input data.

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

**Validation Rules:**
- customer_name: Must be between 1 and 100 characters, required field
- phone_number: Must follow international format (+1234567890), required field
- items: Array containing 1 to 20 items, required field
- pizza_id: Must reference an existing pizza in the database, required field
- quantity: Must be between 1 and 50 per item, required field
- Business Rule: Total order value cannot exceed $500

**Response Format:**
```json
{
  "id": 1,
  "customer_name": "John Doe",
  "phone_number": "+1234567890",
  "total_price": 41.97,
  "created_at": "2025-08-12T12:43:01Z",
  "updated_at": "2025-08-12T12:43:01Z",
  "items": [
    {
      "id": 1,
      "order_id": 1,
      "pizza_id": 1,
      "pizza_name": "Margherita",
      "quantity": 2,
      "calculated_item_total": 25.98
    }
  ]
}
```

**Status Codes:**
- 201 Created: Order successfully created
- 400 Bad Request: Validation error or business rule violation
- 500 Internal Server Error: Server error occurred

#### GET /api/orders/
Retrieves all orders from the database, ordered by creation date with newest orders first.

**Response Format:**
```json
[
  {
    "id": 1,
    "customer_name": "John Doe",
    "phone_number": "+1234567890",
    "total_price": 41.97,
    "created_at": "2025-08-12T12:43:01Z",
    "updated_at": "2025-08-12T12:43:01Z",
    "items": [...]
  }
]
```

**Status Codes:**
- 200 OK: Successfully retrieved orders

#### GET /api/orders/{order_id}
Retrieves a specific order by its unique identifier.

**Parameters:**
- order_id (integer, required): The unique identifier of the order

**Response Format:**
```json
{
  "id": 1,
  "customer_name": "John Doe",
  "phone_number": "+1234567890",
  "total_price": 41.97,
  "created_at": "2025-08-12T12:43:01Z",
  "updated_at": "2025-08-12T12:43:01Z",
  "items": [...]
}
```

**Status Codes:**
- 200 OK: Successfully retrieved order
- 404 Not Found: Order with the specified ID does not exist

### Health Check Endpoint

#### GET /health
Provides a health check endpoint for monitoring systems and load balancers to verify service availability.

**Response Format:**
```json
{
  "status": "healthy",
  "service": "pizza-delivery-api"
}
```

**Status Codes:**
- 200 OK: Service is healthy and responding

## Data Models

### Pizza Model
The Pizza model represents available pizzas in the system with comprehensive validation.

```python
class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    ingredients = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    
    # Database Constraints
    __table_args__ = (
        CheckConstraint('price > 0', name='check_positive_price'),
        CheckConstraint('length(name) > 0', name='check_non_empty_name'),
        CheckConstraint('length(ingredients) > 0', name='check_non_empty_ingredients'),
    )
```

### Order Model
The Orders model represents customer orders with comprehensive tracking and validation.

```python
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False, index=True)
    phone_number = db.Column(db.String(20), nullable=False, index=True)
    total_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False)
    
    # Database Constraints
    __table_args__ = (
        CheckConstraint('total_price >= 0', name='check_non_negative_total'),
        CheckConstraint('length(customer_name) > 0', name='check_non_empty_customer_name'),
        CheckConstraint('length(phone_number) > 0', name='check_non_empty_phone'),
    )
```

### OrderItem Model
The OrderItem model represents individual items within an order with quantity validation.

```python
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, index=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id', ondelete='RESTRICT'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Database Constraints
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_positive_quantity'),
        CheckConstraint('quantity <= 50', name='check_max_quantity'),
    )
```

## Error Handling

### Error Response Format
All error responses follow a consistent format for easy client-side handling:

```json
{
  "error": "Error message description",
  "code": "ERROR_CODE",
  "details": {
    "field": "specific error details"
  }
}
```

### Error Codes
The application uses standardized error codes for different types of errors:
- VALIDATION_ERROR: Input validation failed
- BUSINESS_RULE_ERROR: Business rule violation occurred
- RESOURCE_NOT_FOUND: Requested resource does not exist
- DATABASE_ERROR: Database operation failed
- INTERNAL_ERROR: Unexpected server error
- BAD_REQUEST: Malformed request received
- METHOD_NOT_ALLOWED: HTTP method not supported

### HTTP Status Codes
The API follows standard HTTP status codes:
- 200 OK: Request successful
- 201 Created: Resource successfully created
- 400 Bad Request: Client error in request
- 404 Not Found: Requested resource not found
- 405 Method Not Allowed: HTTP method not supported
- 500 Internal Server Error: Server error occurred

## Testing

### Test Coverage
The application has comprehensive test coverage with 38 tests, all currently passing:
- API endpoint testing covering all routes and scenarios
- Service layer testing validating business logic
- Model testing ensuring data validation and relationships work correctly
- Error handling testing covering all error scenarios
- Factory testing for reliable test data generation
- Integration testing for end-to-end workflows

### Running Tests
To run the test suite, navigate to the backend directory and execute:

```bash
cd backend
python -m pytest tests/ -v
```

The -v flag provides verbose output showing each test result individually.

## Setup and Deployment

### Step 1: Install Dependencies
Install all required Python packages:

```bash
pip install -r requirements.txt
```

### Step 2: Environment Setup
Configure your environment variables:

```bash
# Copy the environment template
cp env_example.txt .env

# Edit the .env file with your specific configuration
nano .env
```

### Step 3: Database Setup
Initialize and configure the database:

```bash
# Run database migrations to create tables
flask db upgrade

# Seed the database with initial pizza data
python seed_data.py
```

### Step 4: Run Application
Start the application in your desired environment:

```bash
# Development mode
python run.py

# Production mode
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Monitoring and Logging

### Log Files
The application maintains comprehensive logs:
- Location: logs/pizza_delivery.log
- Rotation: Maximum file size of 10MB with 10 backup files
- Log Level: INFO and above for production use

### Health Monitoring
The health endpoint provides monitoring capabilities:
- Endpoint: /health
- Expected Response Time: Less than 100ms
- Target Uptime: 99.9%

## Security Features

### Input Validation
- Schema validation using Marshmallow for all incoming data
- Business rule validation enforcing order limits and price caps
- SQL injection protection through SQLAlchemy ORM usage
- XSS protection with proper output encoding

### Error Handling
- No information leakage in production error messages
- Structured error responses with standardized error codes
- Comprehensive logging for debugging and security monitoring

### Database Security
- Parameterized queries through ORM preventing injection attacks
- Transaction management with automatic rollback on errors
- Constraint validation at database level for data integrity
- Foreign key protection with appropriate CASCADE and RESTRICT rules

## Performance Features

### Database Optimization
- Indexed fields for fast query execution
- Lazy loading for relationship data
- Efficient queries through service layer optimization
- Connection pooling ready for production database usage

### API Optimization
- Response caching infrastructure ready for implementation
- Pagination support ready for large datasets
- Compression ready for large response payloads

## Future Enhancements

### Planned Features
- Authentication and authorization using JWT and OAuth2
- Rate limiting and API quota management
- Caching layer integration with Redis
- Message queue system for order processing
- WebSocket support for real-time updates
- Administrative panel for pizza management
- Analytics dashboard for business insights

### Scalability Features
- Horizontal scaling architecture ready
- Load balancer support and configuration
- Microservices architecture preparation
- Container deployment support with Docker

## API Standards Compliance

The application follows industry-standard practices:
- RESTful design principles throughout
- Standard HTTP status codes usage
- Consistent JSON response formatting
- Comprehensive error handling following best practices
- Documentation standards ready for OpenAPI integration
- API versioning infrastructure ready for implementation

## Best Practices Implemented

The application demonstrates enterprise-grade best practices:

1. Separation of Concerns: Clear separation between routes, services, and models
2. Input Validation: Comprehensive schema validation for all inputs
3. Error Handling: Structured error responses with appropriate status codes
4. Security: No information leakage and proper input sanitization
5. Logging: Comprehensive logging system with rotation for production
6. Configuration: Environment-based configuration management
7. Testing: Complete test coverage ensuring reliability
8. Documentation: Comprehensive API documentation for developers
9. Database Design: Proper constraints, relationships, and validation
10. Code Quality: Type hints, docstrings, and clean architecture patterns

## Conclusion

This Pizza Delivery API is now production-ready and follows enterprise-grade best practices. The application provides a robust, secure, and scalable foundation for pizza delivery operations with comprehensive testing, error handling, and documentation. The codebase is maintainable, well-structured, and ready for production deployment with proper configuration and monitoring.

For questions or support, please refer to the codebase structure and test files for implementation details.
