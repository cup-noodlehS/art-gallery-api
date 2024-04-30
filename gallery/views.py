from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Artwork, Category, Bid
from myauth.models import UserProfile
from myauth.serializers import UserProfileSerializer
from .serializers import ArtworkSerializer, CategorySerializer, BidSerializer
from .permissions import IsArtworkOwner, IsBidOwner


class SimpleUserProfileSerializer(UserProfileSerializer):
    class Meta(UserProfileSerializer.Meta):
        fields = ['id', 'avatar_url', 'user']

class ArtworkView(viewsets.ViewSet):
    def list(self, request):
        queryset = Artwork.objects.all()

        filters = {}
        for key in request.query_params.keys():
            filters[key] = request.query_params[key]

        if filters:
            queryset = queryset.filter(**filters)

        objects = ArtworkSerializer(queryset, many=True).data
        objects = [
            {**object, 'artist': SimpleUserProfileSerializer(UserProfile.objects.get(pk=object['artist'])).data}
            for object in objects
        ]

        return Response(objects)

    def retrieve(self, request, pk=None):
        queryset = Artwork.objects.all()
        artwork = get_object_or_404(queryset, pk=pk)
        serialized_artwork = ArtworkSerializer(artwork)
        object = serialized_artwork.data
        serialized_userprofile = UserProfileSerializer(UserProfile.objects.get(pk=artwork.artist.pk))
        object['artist'] = serialized_userprofile.data
        return Response(object)
    
    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [IsArtworkOwner()]
        return []

    def create(self, request):
        serializer = ArtworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        artwork = Artwork.objects.get(pk=pk)
        serializer = ArtworkSerializer(artwork, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        artwork = Artwork.objects.get(pk=pk)
        artwork.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CategoryView(viewsets.ViewSet):
    def list(self, request):
        queryset = Category.objects.all()

        name = request.query_params.get('name')
        if name:
            queryset = queryset.filter(name=name)

        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BidView(viewsets.ViewSet):
    def list(self, request):
        queryset = Bid.objects.all()

        filters = {}
        for key in request.query_params.keys():
            filters[key] = request.query_params[key]

        if filters:
            queryset = queryset.filter(**filters)

        serializer = BidSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Bid.objects.all()
        bid = get_object_or_404(queryset, pk=pk)
        serializer = BidSerializer(bid)
        return Response(serializer.data)
    
    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [IsBidOwner()]
        return []

    def create(self, request):
        serializer = BidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Update the current_highest_bid field in the Artwork model
            highest_bid = Bid.objects.filter(artwork=serializer.data['artwork']).order_by('-bid_amount').first().bid_amount
            if serializer.data['bid_amount'] > highest_bid:
                artwork = Artwork.objects.get(pk=serializer.data['artwork'])
                artwork.current_highest_bid = serializer.data['bid_amount']
                artwork.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        bid = Bid.objects.get(pk=pk)
        serializer = BidSerializer(bid, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        bid = Bid.objects.get(pk=pk)
        bid.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)