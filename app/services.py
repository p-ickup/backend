"""
Service functions for external dependencies.
"""
import logging
import requests
from requests.exceptions import RequestException, Timeout

logger = logging.getLogger(__name__)


def get_prediction(ml_service_url):
    """
    Get a prediction from the ML service.
    
    Args:
        ml_service_url: URL of the ML service
        
    Returns:
        The prediction from the ML service
    
    Raises:
        Exception: If the request fails
    """
    try:
        response = requests.get(f"{ml_service_url}/predict", timeout=10)
        response.raise_for_status()
        return response.json()['prediction']
    except Timeout:
        logger.error("Timeout connecting to ML service")
        raise Exception("ML service timed out")
    except RequestException as e:
        logger.error(f"Error connecting to ML service: {str(e)}")
        raise Exception(f"ML service request failed: {str(e)}")


def check_ml_health(ml_service_url):
    """
    Check the health of the ML service.
    
    Args:
        ml_service_url: URL of the ML service
        
    Returns:
        Dict with health status and details or error
    """
    try:
        response = requests.get(f"{ml_service_url}/health", timeout=10)
        if response.status_code == 200:
            return {
                "status": "available",
                "details": response.json()
            }
        else:
            return {
                "status": "degraded",
                "error": f"Returned status code {response.status_code}"
            }
    except Exception as e:
        return {
            "status": "unavailable",
            "error": str(e)
        }