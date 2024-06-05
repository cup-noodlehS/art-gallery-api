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
    category = models.ForeignKey('gallery.Category', null=True, blank=True, on_delete=models.SET_NULL, related_name='artworks')
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    viewers_count = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN)
    sold_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def current_highest_bid(self):
        highest_bid = self.bids.first()
        if highest_bid:
            return highest_bid.bid_amount
        return None
    
    @property
    def images(self):
        return self.images.all()
    
    @property
    def slug(self):
        alpha_title = ''
        for char in self.title:
            if char.isalnum():
                alpha_title += char.lower()
            elif char == ' ':
                alpha_title += '-'
        return f"{self.pk}-{alpha_title}"

    
    @property
    def first_image(self):
        return self.images.first()
    
    @property
    def bids_count(self):
        return self.bids.count()
    
    @property
    def likes_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    

class ArtworkImage(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()

    def __str__(self):
        return self.artwork.title


class FeaturedArtowrk(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    image_url = models.URLField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['added_on']

    def __str__(self):
        return self.artwork.title
    

class ArtworkNotification(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    members = models.ManyToManyField(User)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.artwork.title