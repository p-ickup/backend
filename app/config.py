"""
Configuration settings for different environments.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Config:
    """Base configuration."""
    SERVICE_NAME = "pickup-backend"
    SERVICE_VERSION = "0.1.0"
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    ML_SERVICE_URL = os.getenv('ML_SERVICE_URL', 'http://ml:5001')
    
    # Supabase configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # In production, make sure these are set and valid
    def __init__(self):
        if not os.getenv('SECRET_KEY'):
            raise ValueError("SECRET_KEY environment variable is not set")
        if not os.getenv('ML_SERVICE_URL'):
            raise ValueError("ML_SERVICE_URL environment variable is not set")


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = False
    TESTING = True
    ML_SERVICE_URL = os.getenv('ML_SERVICE_URL', 'mock://ml-service')