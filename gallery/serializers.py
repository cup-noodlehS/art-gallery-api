from rest_framework import serializers
from .models import Artwork, Category, Bid, ArtworkImage, MessageThread, Message, FeaturedArtowrk
from myauth.serializers import SimpleUserSerializer


class ArtworkImageSerializer(serializers.ModelSerializer):
    artwork = serializers.PrimaryKeyRelatedField(queryset=Artwork.objects.all(), write_only=True)
    class Meta:
        model = ArtworkImage
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    artwork_count = serializers.ReadOnlyField()
    class Meta:
        model = Category
        fields = '__all__'


class ArtworkSerializer(serializers.ModelSerializer):
    current_highest_bid = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    slug = serializers.CharField(read_only=True)
    images = ArtworkImageSerializer(many=True, read_only=True)
    first_image = ArtworkImageSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    artist = SimpleUserSerializer(read_only=True)
    artist_id = serializers.IntegerField(write_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    bids_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Artwork
        fields = '__all__'


class SimpleArtworkSerializer(serializers.ModelSerializer):
    class Meta(ArtworkSerializer.Meta):
        fields = ['id', 'title', 'slug', 'first_image']
    



class BidSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    user_id = serializers.IntegerField()
    class Meta:
        model = Bid
        fields = '__all__'


class MessageThreadSerializer(serializers.ModelSerializer):
    artwork  = SimpleArtworkSerializer()
    class Meta:
        model = MessageThread
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class FeaturedArtowrkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedArtowrk
        fields = '__all__'
