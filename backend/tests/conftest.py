import pytest
from app import create_app
from app.database import db
from config import TestConfig

@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function', autouse=True)
def session(app):
    """Create a clean database session for each test."""
    with app.app_context():
        db.session.begin_nested()
        yield db.session
        db.session.rollback()
        db.session.remove()

@pytest.fixture()
def client(app):
    return app.test_client()
