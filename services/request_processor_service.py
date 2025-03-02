import requests
import logging
from io import BytesIO
from services.image_processor_service import compress_image
from services.file_storage_service import upload_file
from services.database_service import add_request, update_request
from constants.app_constants import AppConstants

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def process_request(request_id, product_name, input_image_url):
    """
    Processes an image request by:
    1. Fetching the image from the URL.
    2. Compressing the image.
    3. Uploading the processed image.
    4. Updating the database with the processed image URL.

    Args:
        request_id (str): Unique request identifier.
        product_name (str): Name of the product associated with the image.
        input_image_url (str): URL of the input image.

    Returns:
        None
    """
    try:
        # Save request before processing
        add_request(request_id, product_name, input_image_url)
        logger.info("Processing request: %s", request_id)

        # Fetch image
        response = requests.get(input_image_url, timeout=10)  # Added timeout for reliability
        if response.status_code != 200:
            logger.error("Failed to fetch image: %s (Status Code: %d)", input_image_url, response.status_code)
            return

        # Process and upload image
        image_payload = BytesIO(response.content)
        compress_ratio = AppConstants.IMAGE_COMPRESS_RATIO

        compressed_image = compress_image(image_payload, compress_ratio)
        if not compressed_image:
            logger.error("Image compression failed for request: %s", request_id)
            return

        output_image_url = upload_file(compressed_image)
        if output_image_url:
            update_request(request_id, product_name, input_image_url, output_image_url)
            logger.info("Request %s processed successfully. Output URL: %s", request_id, output_image_url)
        else:
            logger.error("Image upload failed for request: %s", request_id)

    except requests.RequestException as e:
        logger.error("Network error while fetching image: %s. Error: %s", input_image_url, str(e))
    except Exception as e:
        logger.error("Unexpected error in process_request: %s", str(e))
