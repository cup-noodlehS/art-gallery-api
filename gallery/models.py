from django.db import models
from django.contrib.auth.models import User
from myauth.models import UserProfile


class Artwork(models.Model):
    OPEN = 0
    RESERVED = 1
    SOLD = 2
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (RESERVED, 'Reserved'),
        (SOLD, 'Sold'),
    ]

    artist = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    current_highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN)

    def __str__(self):
        return self.title
    

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Bid(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} bid {self.bid_amount} on {self.artwork.title}'
    

class ArtworkImage(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return self.artwork.title


class MessageThread(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    artist = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='artist')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.artist.user.username} and {self.buyer.user.username} about {self.artwork.title}'
    

class Message(models.Model):
    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.user.username} said {self.body} on {self.sent_on}'