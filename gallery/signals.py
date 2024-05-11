from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from faso.utils import delete_from_cloudinary

from .models import Artwork, MessageThread, Message


@receiver(pre_delete, sender=Artwork)
def delete_artwork_images(sender, instance, **kwargs):
    folder = 'faso/artworks/'
    try:
        for image in instance.images.all():
            image_url = image.image.url
            delete_from_cloudinary(image_url, folder)
    except:
        print('Error deleting images')
    
    print('SUCCESS: Deleted images')
