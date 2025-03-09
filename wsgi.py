"""
WSGI entry point for production servers.
"""
from app.monkey import monkey
import os
import logging
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.getLevelName(os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create the Flask application
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    # Only used for local development
    # In production, this file is used by Gunicorn
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)