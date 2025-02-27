from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)  # NEED THIS to allow frontend to communicate with backend 

ML_SERVICE_URL =  "http://ml:5001"
SERVICE_NAME = "pickup-backend"
SERVICE_VERSION = "0.1.0"
START_TIME = datetime.now()

# Test Route (GET)
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask API!'})

# Test Route (GET) to see if we can get a prediction from the ML model through the backend
@app.route('/api/predict', methods=['GET'])
def predict():
    try:
        # Call the ML API
        response = requests.get(f"{ML_SERVICE_URL}/predict")
        prediction = response.json()['prediction']  # Get prediction from the ML API
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Sending Data from Frontend (POST)
@app.route('/api/send-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    print("Received Data:", data)  # Debugging
    return jsonify({'status': 'success', 'received': data})


# Detailed health check that also tests ML service connectivity
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring and container orchestration"""
    uptime = (datetime.now() - START_TIME).total_seconds()
    
    return jsonify({
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "uptime_seconds": uptime,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    """Detailed health check that includes dependency status"""
    basic_health = health_check().json
    
    # Check ML service connectivity
    ml_status = "unavailable"
    try:
        ml_response = requests.get(f"{ML_SERVICE_URL}/health", timeout=2)
        if ml_response.status_code == 200:
            ml_status = "available"
            ml_details = ml_response.json()
        else:
            ml_details = {"error": f"Returned status code {ml_response.status_code}"}
    except Exception as e:
        ml_details = {"error": str(e)}
    
    return jsonify({
        **basic_health,
        "dependencies": {
            "ml_service": {
                "status": ml_status,
                "url": ML_SERVICE_URL,
                "details": ml_details
            }
        }
    })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
