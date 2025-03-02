from io import BytesIO
from PIL import Image, UnidentifiedImageError
import logging
from constants.app_constants import AppConstants

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def compress_image(image_payload: BytesIO, compress_ratio: int) -> BytesIO:
    """
    Compresses an image while maintaining its quality.

    Args:
        image_payload (BytesIO): The original image file in memory.
        compress_ratio (int): Compression quality (1-100, higher is better quality).

    Returns:
        BytesIO: The compressed image file.
    """
    try:
        input_image = Image.open(image_payload)

        # Convert to RGB to avoid issues with PNG and transparency
        if input_image.mode in ("RGBA", "P"):
            input_image = input_image.convert("RGB")

        output_image = BytesIO()
        input_image.save(output_image, format=AppConstants.IMAGE_COMPRESSION_FORMAT, quality=compress_ratio)

        output_image.seek(0)  # Reset buffer pointer
        logger.info("Image compression successful with ratio: %d", compress_ratio)
        return output_image

    except UnidentifiedImageError:
        logger.error("Invalid image file. Unable to process.")
        return None
    except Exception as e:
        logger.error("Image compression failed: %s", str(e))
        return None
