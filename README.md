# 🍕 Pizza Delivery App - Enterprise Grade

A modern, full-stack pizza delivery application built with Flask backend and React frontend, following enterprise-grade best practices.

## ✨ Features

- **Backend API**: RESTful Flask API with SQLAlchemy ORM
- **Frontend**: Modern React.js with professional UI/UX
- **Database**: SQLite with Alembic migrations
- **Testing**: Comprehensive test suite with 38+ tests
- **Security**: CORS, rate limiting, security headers
- **Documentation**: OpenAPI-style API documentation
- **Error Handling**: Structured error responses
- **Logging**: Production-ready logging system

## 🏗️ Architecture

```
pizza-delivery-app/
├── backend/                 # Flask API Backend
│   ├── app/
│   │   ├── models.py       # SQLAlchemy Models
│   │   ├── routes/         # API Endpoints
│   │   └── services/       # Business Logic
│   ├── migrations/         # Database Migrations
│   ├── tests/              # Test Suite
│   └── config.py           # Configuration
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # React Components
│   │   └── styles/         # CSS Styling
│   └── public/             # Static Assets
└── docs/                   # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- pip
- npm

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Database Setup
```bash
cd backend
flask db upgrade
python seed_data.py
```

## 🧪 Testing

```bash
cd backend
python -m pytest tests/ -v
```

**Test Coverage**: 38+ tests covering:
- API endpoints
- Database models
- Business logic
- Error handling

## 🔒 Security Features

- **CORS Protection**: Configurable origins
- **Security Headers**: XSS, CSRF protection
- **Rate Limiting**: API request throttling
- **Input Validation**: Comprehensive data validation
- **Error Handling**: Secure error responses

## 📚 API Documentation

### Endpoints

#### Pizzas
- `GET /api/pizzas/` - List all pizzas
- `GET /api/pizzas/<id>` - Get specific pizza

#### Orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/` - List all orders
- `GET /api/orders/<id>` - Get specific order

### Health Check
- `GET /health` - Service health status

## 🎨 Frontend Features

- **Modern UI/UX**: Professional design with animations
- **Responsive Design**: Mobile-first approach
- **State Management**: React hooks for state
- **Error Handling**: User-friendly error messages
- **Loading States**: Smooth loading animations

## 🚀 Deployment

### Environment Variables
```bash
FLASK_ENV=production
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
CORS_ORIGINS=https://yourdomain.com
```

### Production Considerations
- Use production WSGI server (Gunicorn)
- Configure reverse proxy (Nginx)
- Set up SSL/TLS certificates
- Monitor with logging and metrics

## 📊 Performance

- **Database**: Optimized queries with indexes
- **Caching**: Ready for Redis integration
- **Frontend**: Optimized bundle with lazy loading
- **API**: Efficient serialization and validation

## 🔧 Development

### Code Quality
- **PEP 8**: Python style guide compliance
- **ESLint**: JavaScript/React linting
- **Type Hints**: Python type annotations
- **Documentation**: Comprehensive docstrings

### Git Workflow
```bash
git add .
git commit -m "feat: add new feature"
git push origin main
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
- Create GitHub issue
- Check documentation
- Review test cases

---

**Built with ❤️ following enterprise best practices**