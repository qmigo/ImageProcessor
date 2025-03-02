import requests
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def is_valid_url(url):
    """Check if the given URL has a valid format."""
    url_regex = re.compile(
        r'^(https?:\/\/)?'  # http:// or https:// (optional)
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6}|'  # Domain name
        r'localhost|'  # Allow localhost
        r'\d{1,3}(\.\d{1,3}){3})'  # Or an IP address
        r'(:\d+)?(\/.*)?$'  # Optional port and path
    )
    return re.match(url_regex, url) is not None

def trigger_webhook(request_id):
    """
    Triggers a webhook by sending a POST request with the request_id and status.

    Args:
        request_id (str): Unique identifier for the request.

    Returns:
        None
    """
    from services.database_service import get_webhook  # Lazy import to avoid circular dependency

    webhook_data = get_webhook(request_id)
    
    if not webhook_data:  
        logger.warning(f"No webhook found for request ID: {request_id}")
        return

    webhook_url = webhook_data.get('webhook_url')  # Extract webhook URL

    if not webhook_url:
        logger.warning(f"Webhook URL missing for request ID: {request_id}")
        return

    if not is_valid_url(webhook_url):
        logger.error(f"Invalid webhook URL for request ID: {request_id} - URL: {webhook_url}")
        return

    payload = {
        "request_id": request_id,
        "status": "completed"
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)

        logger.info(f"Webhook triggered successfully for request ID: {request_id} - Response: {response.status_code}")

    except requests.ConnectionError:
        logger.error(f"Connection error while triggering webhook for request ID: {request_id}")

    except requests.Timeout:
        logger.error(f"Timeout error while triggering webhook for request ID: {request_id}")

    except requests.RequestException as e:
        logger.error(f"Error triggering webhook for request ID: {request_id} - {str(e)}")
