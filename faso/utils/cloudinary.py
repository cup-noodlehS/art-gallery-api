from django.core.files.base import ContentFile
import cloudinary
from cloudinary.uploader import upload

def upload_to_cloudinary(file, folder, width=300, height=300, crop='fill'):
    avatar_urls = []
    crop_params = {
        'width': width,
        'height': height,
        'crop': crop
    }

    try:
        for avatar_file in file:
            image_data = ContentFile(avatar_file.read())            
            uploaded_image = upload(image_data, folder=f"faso/{folder}", **crop_params)
            image_url = uploaded_image['secure_url']
            avatar_urls.append(image_url)
        
        return avatar_urls[0]
    except Exception as e:
        raise e
