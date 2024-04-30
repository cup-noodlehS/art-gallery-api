from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from gallery.models import Artwork
from myauth.models import User
from myauth.serializers import SimpleUserSerializer
from gallery.serializers import ArtworkSerializer
from gallery.permissions import IsArtworkOwner


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
            {**object, 'artist': SimpleUserSerializer(User.objects.get(pk=object['artist'])).data}
            for object in objects
        ]

        return Response(objects)

    def retrieve(self, request, pk=None):
        queryset = Artwork.objects.all()
        artwork = get_object_or_404(queryset, pk=pk)
        serialized_artwork = ArtworkSerializer(artwork)
        object = serialized_artwork.data
        serialized_User = SimpleUserSerializer(User.objects.get(pk=artwork.artist.pk))
        object['artist'] = serialized_User.data
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
    

class TopArtistsView(APIView):
    def get(self, request):
        artworks = Artwork.objects.all().filter(status=Artwork.SOLD).order_by('-current_highest_bid')
        artists = []
        for artwork in artworks:
            if artwork.artist not in artists:
                artists.append(artwork.artist)

        serializer = SimpleUserSerializer(artists, many=True)
        return Response(serializer.data)