from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    '''
    User model contains first_name, last_name, email, username, password
    '''

    SELLER = 0
    BUYER = 1
    USER_TYPE_CHOICES = [
        (SELLER, 'Seller'),
        (BUYER, 'Buyer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.URLField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    address = models.TextField(null=True)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=BUYER)
