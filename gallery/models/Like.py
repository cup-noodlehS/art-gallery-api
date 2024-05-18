from django.db import models
from gallery.models import Artwork
from myauth.models import User


class Like(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.artwork.title}"