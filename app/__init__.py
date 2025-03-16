"""
Flask application factory module.
"""
import os
from flask import Flask
from flask_cors import CORS
from datetime import datetime


def create_app(config_name=None):
    """
    Application factory function that creates and configures the Flask app.
    
    Args:
        config_name: The configuration to use (development, production, testing)
        
    Returns:
        The configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration based on environment
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app.config.from_object(f'app.config.{config_name.capitalize()}Config')
    
    # Initialize extensions
    CORS(app, resources={
    r"/api/*": {
        "origins": ["https://p-ickup.netlify.app", "http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False 
    }
})
    
    # Store app start time for health checks
    app.config['START_TIME'] = datetime.now()
    
    # Register all routes
    from app.routes import register_routes
    from app.health import register_health_routes
    
    register_routes(app)
    register_health_routes(app)
    
    return app