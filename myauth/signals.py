from django.db.models.signals import post_delete
from django.dispatch import receiver
from cloudinary.uploader import destroy

from .models import User
from faso.utils import delete_from_cloudinary


@receiver(post_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    avatar_url = instance.avatar_url
    delete_from_cloudinary(avatar_url)