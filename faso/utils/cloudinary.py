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
    

def delete_from_cloudinary(url):
    public_id = url.split('/')[-1].split('.')[0]
    try:
        result = cloudinary.uploader.destroy(public_id)
        if result['result'] == 'ok':
            print("Image deleted successfully")
            return True
        else:
            print("Error deleting image:", result['message'])
            raise Exception(result['message'])
    except Exception as e:
        print("Error deleting image:", e)
        raise e
