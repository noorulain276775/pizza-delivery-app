"""
Flask application factory for the Pizza Delivery API
"""
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .database import db
from .routes.pizza_routes import pizza_bp
from .routes.order_routes import order_bp
import logging
import os
from logging.handlers import RotatingFileHandler

def create_app(config_name=None):
    """
    Application factory pattern
    
    Args:
        config_name: Configuration name (development, production, testing)
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    
    # Configure CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['http://localhost:3000']))
    
    # Configure logging
    if not app.debug and not app.testing:
        configure_logging(app)
    
    # Register blueprints
    app.register_blueprint(pizza_bp, url_prefix='/api/pizzas')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring"""
        return {'status': 'healthy', 'service': 'pizza-delivery-api'}, 200
    
    return app

def configure_logging(app):
    """Configure application logging"""
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # File handler for production logging
    file_handler = RotatingFileHandler(
        'logs/pizza_delivery.log', 
        maxBytes=10240000, 
        backupCount=10
    )
    
    # Format for log messages
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Configure app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    
    app.logger.info('Pizza Delivery API startup')

def register_error_handlers(app):
    """Register global error handlers"""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors"""
        return {
            'error': 'Bad request',
            'code': 'BAD_REQUEST',
            'message': 'The request could not be processed'
        }, 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors"""
        return {
            'error': 'Not found',
            'code': 'NOT_FOUND',
            'message': 'The requested resource was not found'
        }, 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle method not allowed errors"""
        return {
            'error': 'Method not allowed',
            'code': 'METHOD_NOT_ALLOWED',
            'message': 'The HTTP method is not allowed for this endpoint'
        }, 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle internal server errors"""
        app.logger.error(f'Internal server error: {error}')
        return {
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'message': 'An unexpected error occurred'
        }, 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all unhandled exceptions"""
        app.logger.error(f'Unhandled exception: {error}', exc_info=True)
        return {
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'message': 'An unexpected error occurred'
        }, 500
