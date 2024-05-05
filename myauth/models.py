from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', User.BUYER)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    SELLER = 0
    BUYER = 1
    USER_TYPE_CHOICES = [
        (SELLER, 'Seller'),
        (BUYER, 'Buyer'),
    ]

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, default='Anonymous')
    avatar_url = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    location = models.TextField(null=True, blank=True, max_length=100)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=BUYER)
    achievements = models.TextField(null=True, blank=True, max_length=5000)
    about = models.TextField(null=True, blank=True, max_length=5000)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def user_type_display(self):
        return dict(self.USER_TYPE_CHOICES)[self.user_type]

    objects = CustomUserManager()
