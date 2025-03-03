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