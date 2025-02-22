from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # NEED THIS to allow frontend to communicate with backend 

ML_API_URL = "http://127.0.0.1:5001/predict"

# Test Route (GET)
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask API!'})

# Test Route (GET) to see if we can get a prediction from the ML model through the backend
@app.route('/api/predict', methods=['GET'])
def predict():
    try:
        # Call the ML API
        response = requests.get(ML_API_URL)
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

if __name__ == '__main__':
    app.run(debug=True)
