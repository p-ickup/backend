# Pickup Backend Service

A production-ready Flask API backend for the pickup service, with ML service integration and Supabase authentication.

## 📋 Overview

This repository contains the backend API service for the pickup platform. It handles client requests, integrates with the ML prediction service, and manages authentication through Supabase.

## 🏗 Architecture

The backend uses a Flask application with a modular structure:

- **Flask Application**: Handles HTTP requests and responses
- **ML Client**: Communicates with the ML service for predictions
- **Supabase Integration**: For authentication and database
- **Health Monitoring**: Endpoints for system status and health checks

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Supabase account with project

### Local Development Setup

1. **Clone the repository**

```bash
git clone <repository-url>
cd backend
```

2. **Create a virtual environment (optional for local development)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

   Copy the example environment file:

```bash
cp .env.example .env
```

   Edit `.env` with your configuration values.

5. **Run the development server**

```bash
python app.py
```

   The API will be available at `http://localhost:5000`.

### Using Docker for Development

The recommended way to develop is using the Docker Compose configuration from the infrastructure repository:

```bash
# From the infra repository
docker-compose up
```

This will start both the backend and ML services with hot reloading.

🌐 **API Endpoints**

- **Base API**
  - `GET /api/hello`: Test endpoint
  - `GET /api/predict`: Get prediction from ML service
  - `POST /api/send-data`: Send data for processing

- **Health Endpoints**
  - `GET /health`: Basic health check
  - `GET /health/detailed`: Detailed health check with dependencies

🔧 **Configuration**

### Environment Variables

| Variable                | Description                                     | Default               |
|-------------------------|-------------------------------------------------|-----------------------|
| `FLASK_ENV`             | Environment (development or production)         | development           |
| `SECRET_KEY`            | Secret key for Flask app                        | dev-secret-key (dev only) |
| `ML_SERVICE_URL`        | URL for ML service                              | http://ml:5001        |
| `SUPABASE_URL`          | Supabase project URL                            | None                  |
| `SUPABASE_JWT_SECRET`   | JWT secret for Supabase auth                    | None                  |
| `LOG_LEVEL`             | Logging level                                   | INFO                  |
| `PORT`                  | Port to run the application                     | 5000                  |

🚢 **Deployment**

### Production Deployment

The service is designed to be deployed on AWS ECS Fargate using Docker containers. Key production configurations:

- **WSGI Server**: Uses Gunicorn for handling production traffic
- **Security**: Runs as a non-root user in Docker
- **Environment**: Set `FLASK_ENV=production`
- **Containerization**: Optimized Docker configuration

#### Container Structure

The production container uses:

- Python 3.9 slim base image
- Gunicorn WSGI server
- Multiple workers for concurrency
- Non-root user for security

📁 **Project Structure**

```
Copy/
├── app/                 # Application package
│   ├── __init__.py      # App factory 
│   ├── config.py        # Configuration
│   ├── routes.py        # API routes
│   ├── services.py      # External services (ML client)
│   └── health.py        # Health check endpoints
├── .env.example         # Example environment variables
├── .gitignore           # Git ignore file
├── app.py               # Development entry point
├── wsgi.py              # Production entry point
├── Dockerfile           # Docker configuration
├── entrypoint.sh        # Container entrypoint script
├── gunicorn.conf.py     # Gunicorn configuration
└── requirements.txt     # Dependencies
```

🧪 **Testing**

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app
```

### Testing API Endpoints

To test the API endpoints manually:

```bash
# Test the Hello endpoint
curl -X GET http://localhost:5000/api/hello

# Test the Send Data endpoint
curl -X POST \
  http://localhost:5000/api/send-data \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "user123",
    "pickup_request": {
      "location": {
        "latitude": 37.7749,
        "longitude": -122.4194
      }
    }
  }'
```

📚 **Development Guidelines**

### Code Style

This project follows PEP 8 guidelines. Use tools like flake8 and black for formatting:

```bash
# Check code style
flake8 .

# Format code
black .
```

### Adding New Endpoints

- Define new route functions in `app/routes.py`
- Document API changes in this README
- Add tests for new endpoints

### Environment Configuration

Always add new environment variables to:

- `.env.example` (with example values)
- Documentation in this README
- Appropriate section in `app/config.py`

🔄 **CI/CD Pipeline**

The repository is integrated with a CI/CD pipeline that:

- Runs tests for each PR
- Builds and tags Docker images
- Deploys to staging or production based on branch

🤝 **Integration with Other Services**

### ML Service

The backend integrates with the ML prediction service:

- Communication via HTTP REST API
- Prediction results are returned to clients
- Health checks ensure the ML service is available

### Supabase

Supabase provides:

- User authentication
- Database storage
