from django.db import models
from myauth.models import User
from gallery.models import Artwork


class MessageThread(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artist_message_threads')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_message_threads')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    @property
    def messages(self):
        return Message.objects.filter(thread=self)

    def __str__(self):
        return f'{self.artist.user.username} and {self.buyer.user.username} about {self.artwork.title}'
    

class Message(models.Model):
    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_on']

    def __str__(self):
        return f'{self.sender.user.username} said {self.body} on {self.sent_on}'