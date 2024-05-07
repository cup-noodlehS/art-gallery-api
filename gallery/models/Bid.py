from django.db import models
from myauth.models import User
from gallery.models import Artwork


class Bid(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-bid_amount']

    def __str__(self):
        return f'{self.user.username} bid {self.bid_amount} on {self.artwork.title}'
    

