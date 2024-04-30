from django.contrib import admin
from .models import Artwork, Category, Bid, MessageThread


admin.site.register(Artwork)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(MessageThread)
