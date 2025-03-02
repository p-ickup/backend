"""
Gunicorn configuration for production deployments.
"""
import os
import multiprocessing

# Server socket settings
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
backlog = 2048

# Worker processes
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'gevent'  # Async workers suitable for I/O bound applications
worker_connections = 1000
timeout = 30
keepalive = 2

# Process naming
proc_name = 'pickup-backend'

# Server mechanics
preload_app = True  # Load application code before worker processes are forked

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = os.getenv('LOG_LEVEL', 'info').lower()

# Server hooks
def on_starting(server):
    """Log when server is starting."""
    server.log.info("Starting Pickup Backend API server")

def on_exit(server):
    """Log when server is exiting."""
    server.log.info("Shutting down Pickup Backend API server")