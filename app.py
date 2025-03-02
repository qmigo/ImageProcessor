from flask import Flask, request, jsonify
import concurrent.futures
import uuid
from services.request_processor_service import process_request
from services.file_processor_service import process_file
from exceptions.exceptions import FileNotFoundException
from constants.app_constants import AppConstants

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    file_payload = request.files.get('file')
    if not file_payload:
        raise FileNotFoundException(AppConstants.FILE_NOT_FOUND_EXCEPTION_MSG)

    products = process_file(file_payload)  

    request_id = str(uuid.uuid4())

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(
            lambda product: [
                process_request(request_id, product[AppConstants.PRODUCT_NAME_PARAMETER], img_url)
                for img_url in product[AppConstants.INPUT_IMAGE_URLS_PARAMETER].split(",")
            ], 
            products
        )

    return jsonify({"request_id": request_id}), 202 

if __name__ == '__main__':
    app.run(debug=True, port=5500)