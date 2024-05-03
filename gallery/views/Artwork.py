from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from faso.utils import string_to_list
import json

from gallery.models import Artwork, ArtworkImage, FeaturedArtowrk
from myauth.models import User
from myauth.serializers import SimpleUserSerializer
from gallery.serializers import ArtworkSerializer, ArtworkImageSerializer
from gallery.permissions import IsArtworkOwner


class ArtworkView(viewsets.ViewSet):
    def list(self, request):
        queryset = Artwork.objects.all()

        filters = {}
        excludes = {}
        if request.user:
            excludes['artist_id'] = request.user.id
        print(request.query_params, 'request.query_params')
        for key in request.query_params.keys():
            value = request.query_params[key]
            if ',' in value:
                value = [int(v) for v in value.split(',')]
            filters[key] = value
                

        print(filters, 'filters')

        top = filters.pop('top', 0)
        bottom = filters.pop('bottom', None)
        if top is not None:
            top = int(top)
        if bottom is not None:
            bottom = int(bottom)
        
        size_per_request = 20

        if filters:
            queryset = queryset.filter(**filters).exclude(**excludes)

        objects = ArtworkSerializer(queryset, many=True).data
        if bottom is None:
            bottom = top + size_per_request
        total_count = len(objects)
        objects = objects[top:bottom]

        return Response({
            'total_count': total_count,
            'objects': objects,
        })

    def retrieve(self, request, pk=None):
        queryset = Artwork.objects.all()
        artwork = get_object_or_404(queryset, pk=pk)
        serialized_artwork = ArtworkSerializer(artwork)
        object = serialized_artwork.data
        serialized_User = SimpleUserSerializer(User.objects.get(pk=artwork.artist.pk))
        object['artist'] = serialized_User.data
        artwork.viewers_count += 1
        artwork.save(update_fields=['viewers_count'])
        return Response(object)
    
    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [IsArtworkOwner()]
        return []

    def create(self, request):
        artwork_data = request.data
        image_urls = artwork_data.pop('image_urls', [])
        artwork_serializer = ArtworkSerializer(data=artwork_data)

        with transaction.atomic():
            if artwork_serializer.is_valid():
                artwork_instance = artwork_serializer.save()
            else:
                return Response(artwork_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            image_errors = []
            for image_url in image_urls:
                artwork_image_data = {
                    'artwork': artwork_instance.id,
                    'image_url': image_url
                }
                artwork_image_serializer = ArtworkImageSerializer(data=artwork_image_data)
                if artwork_image_serializer.is_valid():
                    artwork_image_serializer.save()
                else:
                    image_errors.append(artwork_image_serializer.errors)

            if image_errors:
                return Response(image_errors, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            'artwork': artwork_serializer.data,
            'images': ArtworkImageSerializer(ArtworkImage.objects.filter(artwork=artwork_instance.id), many=True).data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    # TODO: Deal with images
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
        artworks = Artwork.objects.all().order_by('-viewers_count')[:10]
        artists = []
        for artwork in artworks:
            if artwork.artist not in artists:
                artists.append(artwork.artist)

        serializer = SimpleUserSerializer(artists, many=True)
        return Response(serializer.data)
    

class FeaturedArtworkView(APIView):
    def get(self, request):
        featured_artworks = FeaturedArtowrk.objects.order_by('-featured_on')[:5]
        artworks = []
        for featured_artwork in featured_artworks:
            artworks.append(featured_artwork.artwork)

        serializer = ArtworkSerializer(artworks, many=True)
        return Response(serializer.data)