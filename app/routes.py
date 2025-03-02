"""
API routes for the application.
"""
import logging
from flask import jsonify, request, current_app
from app.services import get_prediction

logger = logging.getLogger(__name__)


def register_routes(app):
    """Register all API routes on the app."""
    
    @app.route('/api/hello', methods=['GET'])
    def hello():
        """Simple test endpoint."""
        return jsonify({'message': 'Hello from Flask API!'})
    
    @app.route('/api/predict', methods=['GET'])
    def predict():
        """Get a prediction from the ML service."""
        try:
            prediction = get_prediction(current_app.config['ML_SERVICE_URL'])
            return jsonify({"prediction": prediction})
        except Exception as e:
            logger.error(f"Error getting prediction: {str(e)}")
            return jsonify({"error": "Failed to get prediction from ML service"}), 500
    
    @app.route('/api/send-data', methods=['POST'])
    def receive_data():
        """Receive data from the frontend."""
        try:
            data = request.get_json()
            logger.debug(f"Received data: {data}")
            
            # Here you would typically validate and process the data
            # For MVP, we just return success
            
            return jsonify({'status': 'success', 'received': data})
        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            return jsonify({"error": "Failed to process data"}), 400