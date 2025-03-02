from io import BytesIO
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration       
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)


def upload_file(file_payload: BytesIO)->str:
    try:
        response = cloudinary.uploader.upload(
            file_payload,
            resource_type="image",  
            format="jpeg"  
        )
        return response["secure_url"] 
    except Exception as e:
        print("Image upload failed", e)
        return None
