from io import BytesIO
from PIL import Image
from constants.app_constants import AppConstants

def compress_image(image_payload: BytesIO, compress_ratio: int) -> BytesIO:
    input_image = Image.open(image_payload)  

    # Convert to RGB to avoid issues with PNG and transparency
    if input_image.mode in ("RGBA", "P"):
        input_image = input_image.convert("RGB")

    output_image = BytesIO()
    input_image.save(output_image, format=AppConstants.IMAGE_COMPRESSION_FORMAT, quality=compress_ratio)
    
    output_image.seek(0)
    return output_image
