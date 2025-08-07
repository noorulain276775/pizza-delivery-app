# app/__init__.py

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .database import db
from .routes.pizza_routes import pizza_bp

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config:
        app.config.from_object(test_config)
    else:
        app.config.from_object("config.Config")

    CORS(app)
    db.init_app(app)
    Migrate(app, db)
    app.register_blueprint(pizza_bp, url_prefix='/api/pizzas')
    
    return app
