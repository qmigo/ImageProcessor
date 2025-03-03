from flask import Flask, request, jsonify
import concurrent.futures
import uuid
import atexit

# Import necessary services and modules
from services.request_processor_service import process_request
from services.file_processor_service import process_file
from services.database_service import (
    get_request, create_image_processor_request_table, 
    register_webhook, create_webhook_subscription_table
)
from exceptions.exceptions import (
    FileNotFoundException, InvalidRequestException, WebHookNotFoundException
)
from constants.app_constants import AppConstants
from error_handlers import register_error_handlers

# Initialize Flask app
app = Flask(__name__)

# Register custom error handlers
register_error_handlers(app)

# Initialize ThreadPoolExecutor with a defined max worker count
executor = concurrent.futures.ThreadPoolExecutor(max_workers=AppConstants.MAX_THREAD_WORKERS)

# Ensure executor shuts down gracefully on exit
atexit.register(lambda: executor.shutdown(wait=True))

def safe_process_request(request_id, product_name, img_url):
    """
    Safely processes an image request in a separate thread.
    Logs any errors encountered during processing.
    """
    try:
        process_request(request_id, product_name, img_url)
    except Exception as e:
        print(f"Error processing request: {request_id}, Product: {product_name}, Image: {img_url}, Error: {e}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "msg": "Service is running. Kindly check documentation to use application"
    })

@app.route('/upload', methods=['POST'])
def upload():
    """
    Handles file uploads and registers webhooks.
    Processes multiple products and their associated image URLs asynchronously.
    """
    file_payload = request.files.get('file')  # Get uploaded file
    webhook_url = request.form.get('webhook_url')  # Get webhook URL from form data

    # Validate input
    if not file_payload:
        raise FileNotFoundException(AppConstants.FILE_NOT_FOUND_EXCEPTION_MSG)
    if not webhook_url:
        raise WebHookNotFoundException(AppConstants.WEBHOOK_URL_MISSING_ERROR)
    
    products = process_file(file_payload)  # Extract product details from file
    request_id = str(uuid.uuid4())  # Generate unique request ID
    
    register_webhook(webhook_url, request_id)  # Store webhook for request

    # Iterate over extracted products and their images
    for product in products:
        product_name = product[AppConstants.PRODUCT_NAME_PARAMETER]
        image_urls = product[AppConstants.INPUT_IMAGE_URLS_PARAMETER].split(",")

        # Submit each image processing task to the thread pool
        for img_url in image_urls:
            executor.submit(safe_process_request, request_id, product_name, img_url)

    return jsonify({"request_id": request_id}), 202  # Return request ID to client

@app.route('/status/<request_id>', methods=['GET'])
def get_status(request_id: str):
    """
    Fetches the status of a request by request_id.
    Returns the processing status of all associated images.
    """
    if not request_id or len(request_id) != 36:
        raise InvalidRequestException(AppConstants.INVALID_REQUEST_EXCEPTION)
    
    resp = get_request(request_id)  # Retrieve request status from database
    return jsonify({"success": True, "data": resp}), 200

if __name__ == '__main__':
    """
    Initializes the database tables (if they do not exist) and starts the Flask app.
    """
    create_image_processor_request_table()  # Ensure request table exists
    create_webhook_subscription_table()  # Ensure webhook table exists
    app.run(debug=True, port=5500)  # Start Flask server on port 5500
