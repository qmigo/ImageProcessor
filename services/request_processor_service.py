import requests
from io import BytesIO
from services.image_processor_service import compress_image
from services.file_storage_service import upload_file
from services.database_service import add_request, update_request
from constants.app_constants import AppConstants

def process_request(request_id, product_name, input_image_url):
    # Save request before processing
    add_request(request_id, product_name, input_image_url)

    # Fetch image
    response = requests.get(input_image_url)
    if response.status_code != 200:
        return  # No need to proceed if image retrieval fails

    # Process and upload image
    image_payload = BytesIO(response.content)
    compress_ratio = AppConstants.IMAGE_COMPRESS_RATIO
    compressed_image = compress_image(image_payload, compress_ratio)
    output_image_url = upload_file(compressed_image)
    if output_image_url:
        update_request(request_id, product_name, input_image_url, output_image_url)
    