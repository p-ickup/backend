"""
Health check endpoints for monitoring and container orchestration.
"""
import logging
from datetime import datetime
from flask import jsonify, current_app
from app.services import check_ml_health

logger = logging.getLogger(__name__)


def register_health_routes(app):
    """Register health check routes on the app."""
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """
        Basic health check endpoint.
        
        Returns:
            JSON with service status information
        """
        uptime = (datetime.now() - current_app.config['START_TIME']).total_seconds()
        
        return jsonify({
            "status": "healthy",
            "service": current_app.config['SERVICE_NAME'],
            "version": current_app.config['SERVICE_VERSION'],
            "uptime_seconds": uptime,
            "timestamp": datetime.now().isoformat()
        })
    
    @app.route('/health/detailed', methods=['GET'])
    def detailed_health_check():
        """
        Detailed health check that includes dependency status.
        
        Returns:
            JSON with service and dependency status information
        """
        # Get basic health check info
        basic_health = health_check().json
        
        # Check ML service connectivity
        ml_health = check_ml_health(current_app.config['ML_SERVICE_URL'])
        
        return jsonify({
            **basic_health,
            "dependencies": {
                "ml_service": {
                    "status": ml_health["status"],
                    "url": current_app.config['ML_SERVICE_URL'],
                    "details": ml_health.get("details", {"error": ml_health.get("error")})
                }
            }
        })
    
    @app.route('/api/debug-ml-connection', methods=['GET'])
    def debug_ml_connection():
        import socket
        results = {}
        
        # 1. Try DNS resolution
        try:
            hostname = 'ml.prod.p-ickup.internal'
            results['dns_lookup'] = {
                'hostname': hostname,
                'ip': socket.gethostbyname(hostname)
            }
        except Exception as e:
            results['dns_lookup'] = {'error': str(e)}
        
        # 2. Try different service discovery formats
        urls_to_try = [
            'http://ml.prod.p-ickup.internal:5001/health',
            'http://ml:5001/health',
            'http://ml.p-ickup:5001/health',
            'http://ml.prod:5001/health'
        ]
        
        results['connection_tests'] = {}
        for url in urls_to_try:
            try:
                import requests
                # Use a longer timeout
                response = requests.get(url, timeout=10)
                results['connection_tests'][url] = {
                    'status_code': response.status_code,
                    'response': response.text[:100]
                }
            except Exception as e:
                results['connection_tests'][url] = {'error': str(e)}
        
        return jsonify(results)