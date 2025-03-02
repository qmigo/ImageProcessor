from flask import Flask, request, jsonify
import concurrent.futures
import uuid
import atexit
from services.request_processor_service import process_request
from services.file_processor_service import process_file
from services.database_service import get_request, create_image_processor_request_table, register_webhook, create_webhook_subscription_table
from exceptions.exceptions import FileNotFoundException, InvalidRequestException, WebHookNotFoundException
from constants.app_constants import AppConstants
from error_handlers import register_error_handlers

app = Flask(__name__)
register_error_handlers(app)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=AppConstants.MAX_THREAD_WORKERS)
atexit.register(lambda: executor.shutdown(wait=True))


def safe_process_request(request_id, product_name, img_url):
    try:
        process_request(request_id, product_name, img_url)
    except Exception as e:
        print(f"Error processing request: {request_id}, Product: {product_name}, Image: {img_url}, Error: {e}")


@app.route('/upload', methods=['POST'])
def upload():
    file_payload = request.files.get('file')
    webhook_url = request.form.get('webhook_url')

    if not file_payload:
        raise FileNotFoundException(AppConstants.FILE_NOT_FOUND_EXCEPTION_MSG)

    if not webhook_url:
        raise WebHookNotFoundException(AppConstants.WEBHOOK_URL_MISSING_ERROR)
    
    products = process_file(file_payload)  
    request_id = str(uuid.uuid4())
    
    register_webhook(webhook_url, request_id)

    for product in products:
        product_name = product[AppConstants.PRODUCT_NAME_PARAMETER]
        image_urls = product[AppConstants.INPUT_IMAGE_URLS_PARAMETER].split(",")

        for img_url in image_urls:
            executor.submit(safe_process_request, request_id, product_name, img_url)

    return jsonify({"request_id": request_id}), 202


@app.route('/status/<request_id>', methods=['GET'])
def get_status(request_id: str):
    if not request_id or len(request_id) != 36:
        raise InvalidRequestException(AppConstants.INVALID_REQUEST_EXCEPTION)
    
    resp = get_request(request_id)
    return jsonify({"success": True, "data": resp}), 200


if __name__ == '__main__':
    create_image_processor_request_table()
    create_webhook_subscription_table()
    app.run(debug=True, port=5500)
