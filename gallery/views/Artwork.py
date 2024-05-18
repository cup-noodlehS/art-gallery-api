from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import datetime

from gallery.models import Artwork, ArtworkImage, FeaturedArtowrk
from myauth.models import User
from myauth.serializers import SimpleUserSerializer
from gallery.serializers import ArtworkSerializer, ArtworkImageSerializer, FeaturedArtowrkSerializer
from gallery.permissions import IsArtworkOwner


class ArtworkView(viewsets.ViewSet):
    permission_classes = [IsArtworkOwner]
    def list(self, request):
        queryset = Artwork.objects.all()

        filters = {}
        excludes = {}
        # if request.user:
        #     excludes['artist_id'] = request.user.id
        for key in request.query_params.keys():
            value = request.query_params[key]
            if ',' in value:
                value = [int(v) for v in value.split(',')]
            filters[key] = value
                

        search_key = filters.pop('search_key', None)
        order = filters.pop('order_by', None)

        top = filters.pop('top', 0)
        bottom = filters.pop('bottom', None)
        if top != 0:
            top = int(top)
        if bottom is not None:
            bottom = int(bottom)
        
        size_per_request = 21

        if search_key is not None:
                search_key = search_key.lower()
                queryset = queryset.filter(
                    Q(title__icontains=search_key) | 
                    Q(artist__username__icontains=search_key)
                )
        if order is not None:
            queryset = queryset.order_by(order)

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
        print(request.user, 'request.user')
        queryset = Artwork.objects.all()
        artwork = get_object_or_404(queryset, pk=pk)
        serialized_artwork = ArtworkSerializer(artwork)
        object = serialized_artwork.data
        serialized_User = SimpleUserSerializer(User.objects.get(pk=artwork.artist.pk))
        object['artist'] = serialized_User.data
        if not request.user or request.user.id != artwork.artist_id:
            artwork.viewers_count += 1
            artwork.save(update_fields=['viewers_count'])
        return Response(object)

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
        artworks = Artwork.objects.filter(created_on__gte=datetime.date.today() - datetime.timedelta(days=30))\
                    .order_by('-viewers_count')
        artists = []
        for artwork in artworks:
            if len(artists) == 10:
                break
            if artwork.artist not in artists:
                artists.append(artwork.artist)

        serializer = SimpleUserSerializer(artists, many=True)
        return Response(serializer.data)
    

class FeaturedArtworkView(APIView):
    def get(self, request):
        featured_artworks = FeaturedArtowrk.objects.filter(date__lte=datetime.date.today()).order_by('-added_on')[:5]
        serializer = FeaturedArtowrkSerializer(featured_artworks, many=True)
        return Response(serializer.data)