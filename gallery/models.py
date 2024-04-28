from django.db import models
from django.contrib.auth.models import User

class Artwork(models.Model):
    OPEN = 0
    RESERVED = 1
    SOLD = 2
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (RESERVED, 'Reserved'),
        (SOLD, 'Sold'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    current_highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
