import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///pizzas.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security - No default secret key for production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # API Settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Rate Limiting
    RATE_LIMIT_DEFAULT = os.environ.get('RATE_LIMIT_DEFAULT', '200 per day, 50 per hour')
    RATE_LIMIT_CHAT = os.environ.get('RATE_LIMIT_CHAT', '20 per minute')
    
    # AI Model Configuration
    AI_MODEL_NAME = os.environ.get('AI_MODEL_NAME', 'microsoft/DialoGPT-medium')
    AI_MAX_LENGTH = int(os.environ.get('AI_MAX_LENGTH', '100'))
    AI_TEMPERATURE = float(os.environ.get('AI_TEMPERATURE', '0.7'))
    
    def __init__(self):
        print(f"Config initialized with AI_MODEL_NAME: {self.AI_MODEL_NAME}")
        print(f"Config initialized with AI_MAX_LENGTH: {self.AI_MAX_LENGTH}")
        print(f"Config initialized with AI_TEMPERATURE: {self.AI_TEMPERATURE}")

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'
    
    # Development-specific secret key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Production security settings - Must be set via environment
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Ensure HTTPS in production
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    
    # Production validation
    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError('SECRET_KEY must be set in production')
        if not self.SQLALCHEMY_DATABASE_URI:
            raise ValueError('DATABASE_URL must be set in production')

class TestConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}
