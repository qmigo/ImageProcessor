from io import BytesIO
import cloudinary
import cloudinary.uploader
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Cloudinary Configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_file(file_payload: BytesIO) -> str:
    """
    Uploads an image file to Cloudinary.

    Args:
        file_payload (BytesIO): The image file in memory.

    Returns:
        str: The secure URL of the uploaded image if successful, otherwise None.
    """
    try:
        response = cloudinary.uploader.upload(
            file_payload,
            resource_type="image",  # Specify that the file is an image
            format="jpeg"  # Convert file format to JPEG
        )
        logger.info("Image successfully uploaded: %s", response["secure_url"])
        return response["secure_url"]
    
    except Exception as e:
        logger.error("Image upload failed: %s", str(e))
        return None
