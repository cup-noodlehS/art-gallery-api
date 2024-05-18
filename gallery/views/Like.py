from rest_framework.response import Response
from rest_framework import status

from gallery.models import Like
from gallery.serializers import LikeSerializer
from rest_framework import viewsets


class LikeView(viewsets.ViewSet):
    def list(self, request):
        queryset = Like.objects.all()
        filters = {}

        for key in request.query_params.keys():
            filters[key] = request.query_params[key]
        
        top = int(filters.pop('top', 0))
        size_per_request = 20

        if filters:
            queryset = queryset.filter(**filters)

        objects = LikeSerializer(queryset, many=True).data
        total_count = len(objects)
        objects = objects[top:top + size_per_request]

        return Response({
            'total_count': total_count,
            'objects': objects
        })
    
    def retrieve(self, request, pk=None):
        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        object = Like.objects.get(pk=pk)
        serialized = LikeSerializer(object)
        return Response(serialized.data)
    
    def create(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        like = Like.objects.get(pk=pk)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)