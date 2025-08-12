"""
Flask application factory for Pizza Delivery API
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from .database import db
from config import config

def create_limiter():
    """Create and configure rate limiter"""
    return Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    config_obj = config[config_name]()
    for key in dir(config_obj):
        if not key.startswith('_') and not callable(getattr(config_obj, key)):
            app.config[key] = getattr(config_obj, key)
    
    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    
    # Create and initialize rate limiter with app
    limiter = create_limiter()
    limiter.init_app(app)
    
    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS')}})
    
    # Import routes after limiter is initialized to avoid circular imports
    from .routes.pizza_routes import pizza_bp
    from .routes.order_routes import order_bp
    from .routes.chat_routes import chat_bp
    
    # Register blueprints
    app.register_blueprint(pizza_bp, url_prefix='/api/pizzas')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Add security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Dynamic CSP based on environment
        if app.config.get('FLASK_ENV') == 'production':
            response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self';"
        else:
            response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' http://127.0.0.1:5000;"
        
        return response
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'service': 'pizza-delivery-api',
            'timestamp': app.config.get('TIMESTAMP', 'N/A'),
            'environment': app.config.get('FLASK_ENV', 'development')
        })
    
    # Configure logging
    configure_logging(app)
    
    return app

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not Found', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal Server Error', 'message': 'Something went wrong'}), 500
    
    @app.errorhandler(413)
    def payload_too_large(error):
        return jsonify({'error': 'Payload Too Large', 'message': 'Request body too large'}), 413
    
    @app.errorhandler(429)
    def too_many_requests(error):
        return jsonify({'error': 'Too Many Requests', 'message': 'Rate limit exceeded'}), 429

def configure_logging(app):
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Pizza Delivery startup')
