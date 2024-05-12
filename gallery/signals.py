from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from faso.utils import delete_from_cloudinary

from .models import Artwork, MessageThread, Message, ArtworkImage


# @receiver(post_delete, sender=Artwork)
# def delete_artwork_images(sender, instance, **kwargs):
#     folder = 'faso/artworks/'
#     print('HEREEE', instance)
#     try:
#         for image in instance.images.all():
#             image_url = image.image.url
#             delete_from_cloudinary(image_url, folder)
#     except:
#         print('Error deleting images')
    
#     print('SUCCESS: Deleted images')
@receiver(post_delete, sender=ArtworkImage)
def delete_artwork_image(sender, instance, **kwargs):
    folder = 'faso/artworks/'
    try:
        delete_from_cloudinary(instance.image_url, folder)
    except:
        print('Error deleting image')
    
    print('SUCCESS: Deleted image')