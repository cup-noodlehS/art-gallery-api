from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Artwork, MessageThread, Message
from myauth.models import UserProfile


@receiver(post_save, sender=Artwork)
def create_message_thread(sender, instance, created, **kwargs):
    if not created:
        if instance.status == Artwork.RESERVED:
            thread = MessageThread.objects.get_or_create(artwork=instance, artist=instance.artist, buyer=instance.buyer)
            messages = Message.objects.filter(thread=thread)
            if not messages:
                Message.objects.create(thread=thread, sender=instance.artist, message=f'{instance.title} is now reserved for {instance.buyer.user.username}')
