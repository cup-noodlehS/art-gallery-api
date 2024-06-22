from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class GenericView(viewsets.ViewSet):
    queryset = None
    serializer_class = None
    size_per_request = 20
    permission_classes = []
    instance_method_fields = []

    cache_key = None
    cache_duration = 60 * 60  
    
    # CRUD operations
    def list(self, request):
        filters = {}
        excludes = {}
        for key in request.query_params.keys():
            value = request.query_params[key]
            if key[-4:] == '__in':
                value = [int(v) for v in value.split(',')]
            filters[key] = value

        top = int(filters.pop('top', 0))
        bottom = filters.pop('bottom', None)
        if bottom:
            bottom = int(bottom)
        else:
            bottom = top + self.size_per_request
        
        return self.filter(request, filters, excludes, top, bottom)
    
    def retrieve(self, request, pk=None):
        object = self.get_serialized_object(pk)
        return Response(object, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        object = self.queryset.get_object_or_404(pk=pk)
        serializer = self.serializer_class(object, data=request.data)
        if serializer.is_valid():
            self.delete_cache(pk)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        object = self.query_set.get_object_or_404(pk=pk)
        self.delete_cache(pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # END CRUD operations

    # Cache operations
    def delete_cache(self, pk):
        pass

    def cache_queryset(self, queryset):
        pass

    def cache_object(self, object, pk):
        pass
    # END Cache operations

    # Helper methods
    def filter_queryset(self, filters, excludes, *args, **kwargs):
        return self.queryset.filter(**filters).exclude(**excludes)
    
    def filter(self, request, filters, excludes, top, bottom, *args, **kwargs):
        queryset = self.filter_queryset(filters, excludes)
            
        total_count = len(queryset)
        objects = self.queryset[top:bottom].serializer_class(queryset, many=True).data

        return Response({
            'objects': objects,
            'total_count': total_count
        }, status=status.HTTP_200_OK)
    
    def get_serialized_object(self, pk):
        # use caching soon
        return self.serializer_class(get_object_or_404(self.queryset, pk=pk)).data
    
    # END Helper methods
