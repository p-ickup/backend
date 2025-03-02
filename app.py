"""
Development entry point for Flask application.
"""
import os
from app import create_app

# Create the Flask application with development configuration
app = create_app('development')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)