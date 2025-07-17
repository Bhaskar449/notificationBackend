import os
from dotenv import load_dotenv
import secrets

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg://bhaskarjoshi@localhost:5432/flask_backend_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
    
class DevelopmentConfig(Config):
    DEBUG = True
    # Use fixed keys for development to avoid token invalidation on restart
    SECRET_KEY = 'dev-secret-key-flask-backend-2024'
    JWT_SECRET_KEY = 'dev-jwt-secret-key-flask-backend-2024'
    
class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret-key'
    JWT_SECRET_KEY = 'test-jwt-secret-key'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 