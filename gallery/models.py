from django.db import models
from myauth.models import User


class Artwork(models.Model):
    OPEN = 0
    RESERVED = 1
    SOLD = 2
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (RESERVED, 'Reserved'),
        (SOLD, 'Sold'),
    ]

    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artworks_created')
    buyer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='artworks_bought')
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN)

    @property
    def current_highest_bid(self):
        highest_bid = self.bids.first()
        if highest_bid:
            return highest_bid.bid_amount
        return 0
    
    @property
    def images(self):
        return self.images.all()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    

class FeaturedArtowrk(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    featured_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-featured_on']

    def __str__(self):
        return self.artwork.title
    

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    @property
    def artwork_count(self):
        return Artwork.objects.filter(category=self).count()

    def __str__(self):
        return self.name
    

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
    

class ArtworkImage(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()

    def __str__(self):
        return self.artwork.title


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