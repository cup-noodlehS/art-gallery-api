from django.contrib import admin
from .models import Artwork, Category, Bid, MessageThread, ArtworkImage, FeaturedArtowrk, Like

class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 0

class FeaturedArtworkInline(admin.TabularInline):
    model = FeaturedArtowrk
    extra = 0

class ArtworkAdmin(admin.ModelAdmin):
    inlines = [ArtworkImageInline, FeaturedArtworkInline]
    list_display = ('title', 'artist', 'status', 'current_highest_bid', 'created_on')  # Corrected 'price' to 'current_highest_bid'
    list_filter = ('status',)
    search_fields = ('title', 'artist__username')

admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(MessageThread)
admin.site.register(FeaturedArtowrk)
admin.site.register(ArtworkImage)
admin.site.register(Like)
