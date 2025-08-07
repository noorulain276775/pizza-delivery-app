class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pizzas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory DB for testing
    TESTING = True
