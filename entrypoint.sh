#!/bin/bash
set -e

# Environment can be 'development' or 'production'
ENVIRONMENT=${FLASK_ENV:-production}

echo "Starting Flask application in $ENVIRONMENT mode"

if [ "$ENVIRONMENT" = "development" ]; then
    # Development mode: use Flask's built-in server with hot reloading
    exec python app.py
else
    # Production mode: use Gunicorn
    echo "Starting with Gunicorn..."
    exec gunicorn --bind 0.0.0.0:5000 \
        --workers 2 \
        --threads 2 \
        --timeout 60 \
        --access-logfile - \
        --error-logfile - \
        wsgi:app
fi