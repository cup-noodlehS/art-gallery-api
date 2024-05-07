from django.db import models
from gallery.models import Artwork

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    @property
    def artwork_count(self):
        return Artwork.objects.filter(category=self).count()

    def __str__(self):
        return self.name