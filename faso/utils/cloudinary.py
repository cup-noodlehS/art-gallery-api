from django.core.files.base import ContentFile
import cloudinary
from cloudinary.uploader import upload

def upload_to_cloudinary(file, folder, width=300, height=300, crop='fill'):
    crop_params = {
        'width': width,
        'height': height,
        'crop': crop
    }

    try:
        # Read the file data and create a ContentFile object
        image_data = ContentFile(file.read())
        
        # Upload image to Cloudinary
        uploaded_image = upload(image_data, folder=f"faso/{folder}", **crop_params)
        image_url = uploaded_image['secure_url']
        
        return image_url
    except Exception as e:
        raise e
    

def delete_from_cloudinary(url, folder):
    public_id = folder + url.split('/')[-1].split('.')[0]
    try:
        result = cloudinary.uploader.destroy(public_id)
        if result['result'] == 'ok':
            print("Image deleted successfully")
            return result
        else:
            print("Error deleting image:", result)
            raise Exception(result['message'])
    except Exception as e:
        print("Error deleting image:", e)
        raise e
