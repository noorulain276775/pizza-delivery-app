# Pizza Delivery Application with AI Powered Customer Support

A full-stack pizza delivery application with AI-powered customer support, built using Flask backend and React frontend. This project demonstrates enterprise-grade architecture, modern development practices, and cutting-edge AI integration.

## Features

### Core Functionality
- **Pizza Management**: Browse available pizzas with high-quality images and descriptions
- **Shopping Cart**: Interactive cart with real-time updates and quantity management
- **Order Processing**: Cash-on-delivery orders with customer information
- **Responsive Design**: Mobile-first approach with modern UI/UX
- **Real-time Updates**: Live cart totals and order status

### AI-Powered Customer Support
- **Intelligent Chatbot**: Built with Hugging Face Transformers using DialoGPT-medium
- **Natural Language Understanding**: Handles customer queries about menu, pricing, delivery, and payment
- **Context-Aware Responses**: Maintains conversation history for personalized interactions
- **Domain-Specific Knowledge**: Specialized in pizza delivery business logic
- **Fallback Mechanisms**: Rule-based responses when AI is unavailable
- **Multi-session Support**: Separate chat sessions for different users

### Technical Excellence
- **RESTful API**: Comprehensive error handling and validation
- **Database Migrations**: Alembic with SQLAlchemy ORM
- **Testing Suite**: 38+ tests with Factory Boy and Pytest
- **Security**: Rate limiting, security headers, and CORS configuration
- **Performance**: React optimization, database indexing, and AI response caching
- **Logging**: Production-ready logging and monitoring

## Architecture

### Backend (Flask)
```
backend/
├── app/
│   ├── models.py          # SQLAlchemy models with validation
│   ├── routes/            # API endpoints with rate limiting
│   ├── services/          # Business logic and AI service layer
│   └── __init__.py        # Flask app factory with extensions
├── migrations/            # Database schema changes
├── tests/                 # Comprehensive test suite
└── requirements.txt       # Python dependencies
```

### Frontend (React)
```
frontend/
├── src/
│   ├── components/        # Modular, reusable components
│   ├── hooks/            # Custom React hooks for state management
│   ├── config.js         # API configuration and utilities
│   └── App.js            # Main application composition
├── public/               # Static assets and images
└── package.json          # Node.js dependencies
```

## Technology Stack

### Backend
- **Flask**: Modern web framework with blueprints
- **SQLAlchemy**: Advanced ORM with migrations
- **Flask-Migrate**: Database schema management
- **Hugging Face Transformers**: State-of-the-art AI models
- **PyTorch**: Deep learning framework
- **Pytest**: Comprehensive testing framework
- **Factory Boy**: Test data generation
- **Flask-Limiter**: API rate limiting and protection

### Frontend
- **React**: Modern UI library with hooks
- **Custom Hooks**: Optimized state management
- **Axios**: HTTP client with error handling
- **Modern CSS**: Glass morphism, CSS Grid, and animations
- **PropTypes**: Runtime type checking and validation

## Prerequisites

- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **Git**: Version control system
- **Memory**: 2GB RAM minimum (4GB recommended for AI models)
- **Storage**: 2GB free space for AI models

## Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd pizza-delivery-app
```

### 2. Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install AI-specific dependencies
pip install torch transformers tokenizers

# Setup database
flask db upgrade

# Start backend server
python run.py
```

**Backend will be available at**: `http://127.0.0.1:5000`

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

**Frontend will be available at**: `http://localhost:3000`

### 4. Verify Installation
```bash
# Backend health check
curl http://127.0.0.1:5000/health

# AI chatbot health check
curl http://127.0.0.1:5000/api/chat/health
```

## API Configuration & Endpoints

### Frontend API Configuration
The frontend connects directly to the backend API using a configurable base URL instead of proxy settings.

#### Default Configuration
By default, the frontend connects to: `http://127.0.0.1:5000`

#### Environment Variable Configuration
To change the backend URL, set the `REACT_APP_API_URL` environment variable:

**Unix/Linux/Mac:**
```bash
export REACT_APP_API_URL=http://your-backend-ip:5000
npm start
```

**Windows:**
```cmd
set REACT_APP_API_URL=http://your-backend-ip:5000
npm start
```

#### Configuration File
The main configuration is in `frontend/src/config.js`:

```javascript
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000',
  ENDPOINTS: {
    PIZZAS: '/api/pizzas/',
    ORDERS: '/api/orders/',
    CHAT: '/api/chat/chat',
    HEALTH: '/health'
  }
};
```

#### Use Cases
- **Development**: Local backend at `http://127.0.0.1:5000` (default)
- **Production**: Production backend at `https://api.yourdomain.com`
- **Staging**: Staging backend at `https://staging-api.yourdomain.com`

### API Endpoints

#### Pizza Management
- `GET /api/pizzas/` - List all available pizzas
- `GET /api/pizzas/<id>` - Get specific pizza details

#### Order Management
- `POST /api/orders/` - Create new order
- `GET /api/orders/` - List all orders
- `GET /api/orders/<id>` - Get specific order details

#### AI Chatbot
- `POST /api/chat/chat` - Send message to AI chatbot
- `GET /api/chat/history/<session_id>` - Get chat history
- `DELETE /api/chat/clear/<session_id>` - Clear chat history
- `GET /api/chat/stats` - Get usage statistics
- `GET /api/chat/health` - Check chatbot health
- `GET /api/chat/help` - API documentation

## AI Chatbot Implementation

### Technical Architecture
The AI chatbot uses a sophisticated multi-layered architecture:

```
AI Chatbot System
├── Backend Service Layer
│   ├── AI Service (PizzaAIService)
│   ├── Chat Routes (chat_bp)
│   └── Rate Limiting (Flask-Limiter)
├── AI Model Layer
│   ├── Hugging Face Transformers
│   ├── DialoGPT-medium Model (345M parameters)
│   └── Tokenizer & Pipeline
├── Frontend Integration
│   ├── React Chatbot Component
│   ├── Real-time Messaging
│   └── Session Management
└── Data Layer
    ├── Conversation History
    ├── Session Storage
    └── Performance Metrics
```

### AI Model Details
- **Model**: Microsoft DialoGPT-medium
- **Parameters**: 345M for high-quality responses
- **Training**: Reddit conversations for natural dialogue
- **Context**: 1024 tokens for conversation memory
- **Performance**: 1-3 seconds response time

### Capabilities
- **Menu Information**: Detailed pizza descriptions, ingredients, and pricing
- **Delivery Queries**: Timing, costs, policies, and service areas
- **Payment Support**: Accepted methods and policies
- **Order Assistance**: Status tracking and modifications
- **General Support**: Customer service and FAQ assistance

### Example Interactions
```
User: "What pizzas do you have?"
Bot: "We offer Margherita Pizza with classic tomato and mozzarella, 
      Pepperoni Pizza with spicy pepperoni and cheese, and 
      Vegetarian Pizza with fresh vegetables and cheese."

User: "How long does delivery take?"
Bot: "Standard delivery takes 30-45 minutes, while express delivery 
      takes 20-30 minutes with an additional $3 fee. 
      Free delivery is available on orders over $25."
```

## Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Test Coverage
- **Unit Tests**: Models, services, and utilities
- **Integration Tests**: API endpoints and database operations
- **Factory-based Testing**: Comprehensive test data generation
- **Error Scenarios**: Edge cases and failure handling

## Security Features

- **Rate Limiting**: API request throttling (20/minute for chat, 50/hour general)
- **Security Headers**: XSS protection, content type validation
- **Input Validation**: Comprehensive data sanitization
- **CORS Configuration**: Controlled cross-origin access
- **Error Handling**: Secure error messages without information leakage

## Performance Optimizations

### Backend
- **Database Indexing**: Optimized queries with proper indexes
- **AI Response Caching**: Reduced generation time for common queries
- **Connection Pooling**: Efficient database connections
- **Async Processing**: Non-blocking AI model operations

### Frontend
- **React Memoization**: Prevents unnecessary re-renders
- **Custom Hooks**: Optimized state management
- **Code Splitting**: Dynamic imports for better performance
- **Asset Optimization**: Compressed images and fonts

## Deployment

### Environment Variables
```bash
# Backend (.env)
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://yourdomain.com
LOG_LEVEL=INFO

# Frontend (.env)
REACT_APP_API_URL=https://your-backend-domain.com
```

### Production Considerations
- **Database**: Use PostgreSQL or MySQL for production
- **Web Server**: Gunicorn with Nginx reverse proxy
- **SSL/TLS**: Enable HTTPS with proper certificates
- **Monitoring**: Implement logging and performance metrics
- **Backup Strategy**: Regular database and file backups

## Development Workflow

### Code Quality
- **PEP 8**: Python style guide compliance
- **ESLint**: JavaScript/React code quality
- **Type Safety**: PropTypes for runtime validation
- **Documentation**: Comprehensive docstrings and comments

### Git Workflow
```bash
# Feature development
git checkout -b feature/ai-chatbot
git add .
git commit -m "feat: implement AI chatbot with Hugging Face"
git push origin feature/ai-chatbot

# Create pull request for review
```

## Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check port availability
lsof -i :5000

# Verify virtual environment
source .venv/bin/activate

# Check dependencies
pip list | grep flask
```

#### AI Models Not Loading
```bash
# Verify internet connection
ping huggingface.co

# Check model cache
ls -la ~/.cache/huggingface/

# Reinstall AI dependencies
pip uninstall torch transformers tokenizers
pip install torch transformers tokenizers
```

#### Frontend Connection Issues
```bash
# Check backend health
curl http://127.0.0.1:5000/health

# Verify CORS configuration
# Check browser console for errors

# Test different backend URLs
export REACT_APP_API_URL=http://192.168.1.100:5000
npm start
```

#### API Configuration Issues
- **Connection Refused**: Check if backend is running on the specified URL
- **CORS Errors**: Ensure backend CORS is configured for the frontend URL
- **404 Errors**: Verify the backend endpoints are accessible
- **Environment Variables**: Restart frontend after changing `REACT_APP_API_URL`

### Debug Commands
```bash
# Backend debugging
tail -f backend/logs/app.log

# AI service test
python -c "
from app.services.ai_service import PizzaAIService
ai = PizzaAIService()
print(ai.generate_response('Hello', 'test'))
"

# Frontend debugging
# Use React DevTools and browser console
```

## Monitoring & Analytics

### Performance Metrics
- **Response Times**: API and AI response latency
- **Error Rates**: Failure and fallback percentages
- **Usage Statistics**: Conversation counts and user engagement
- **Resource Usage**: Memory and CPU utilization

### Health Checks
```bash
# Service health
curl http://127.0.0.1:5000/health

# AI chatbot status
curl http://127.0.0.1:5000/api/chat/health

# Performance stats
curl http://127.0.0.1:5000/api/chat/stats
```

## Future Enhancements

### Planned Features
- **Multi-language Support**: International customer support
- **Voice Integration**: Speech-to-text and text-to-speech
- **Advanced Analytics**: Customer behavior insights
- **Mobile App**: Native iOS and Android applications

### Technical Improvements
- **TypeScript**: Enhanced type safety for frontend
- **GraphQL**: Advanced API querying capabilities
- **Microservices**: Scalable architecture evolution
- **Kubernetes**: Container orchestration for production

## Support

### Documentation
- **API Reference**: Check individual endpoint documentation
- **Component Guide**: Frontend component descriptions
- **AI Implementation**: Detailed chatbot architecture

### Resources
- **Flask Documentation**: https://flask.palletsprojects.com/
- **React Documentation**: https://reactjs.org/docs/
- **Hugging Face**: https://huggingface.co/docs/transformers/
- **PyTorch Tutorials**: https://pytorch.org/tutorials/

---

**Built with modern technologies and best practices for enterprise-grade applications**