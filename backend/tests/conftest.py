import pytest
from app import create_app
from app.database import db
import os

@pytest.fixture(scope='function')
def app():
    """Create a fresh app instance for each test."""
    # Set testing environment
    os.environ['FLASK_ENV'] = 'testing'
    
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function', autouse=True)
def session(app):
    """Create a clean database session for each test."""
    with app.app_context():
        # Clear any existing data
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()
