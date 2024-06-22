from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction

class GenericView(viewsets.ViewSet):
    queryset = None
    serializer_class = None
    size_per_request = 20
    permission_classes = []
    instance_method_fields = []

    cache_key_prefix = None
    cache_duration = 60 * 60  # 1 hour

    # CRUD operations
    def list(self, request):
        try:
            filters, excludes = self.parse_query_params(request)
            top, bottom = self.get_pagination_params(filters)
        
            cached_data = None    
            if self.cache_key_prefix:
                cache_key = self.get_list_cache_key(filters, excludes, top, bottom)
                cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data, status=status.HTTP_200_OK)
            
            return self.filter(request, filters, excludes, top, bottom)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        cached_object = None
        if self.cache_key_prefix:
            cache_key = self.get_object_cache_key(pk)
            cached_object = cache.get(cache_key)
        if cached_object:
            return Response(cached_object, status=status.HTTP_200_OK)
        
        object = self.get_serialized_object(pk)
        self.cache_object(object, pk)
        return Response(object, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            self.cache_object(serializer.data, instance.pk)
            self.invalidate_list_cache()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.cache_object(serializer.data, pk)
            self.invalidate_list_cache()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        self.delete_cache(pk)
        self.invalidate_list_cache()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Cache operations
    def delete_cache(self, pk):
        if not self.cache_key_prefix:
            return
        cache_key = self.get_object_cache_key(pk)
        cache.delete(cache_key)

    def invalidate_list_cache(self):
        if not self.cache_key_prefix:
            return
        cache.delete_pattern(f"{self.cache_key_prefix}_list_*")

    def cache_object(self, object_data, pk):
        if not self.cache_key_prefix:
            return
        cache_key = self.get_object_cache_key(pk)
        cache.set(cache_key, object_data, self.cache_duration)

    def get_object_cache_key(self, pk):
        return f"{self.cache_key_prefix}_object_{pk}"

    def get_list_cache_key(self, filters, excludes, top, bottom):
        return f"{self.cache_key_prefix}_list_{hash(frozenset(filters.items()))}_" \
               f"{hash(frozenset(excludes.items()))}_{top}_{bottom}"

    # Helper methods
    def parse_query_params(self, request):
        filters = {}
        excludes = {}

        def parse_list_parameter(value):
            values = [v.strip() for v in value.rstrip(',').split(',') if v.strip()]
            return values if len(values) > 1 else values[0] if values else None

        for key, value in request.query_params.items():
            if key.startswith('exclude__'):
                parsed_value = parse_list_parameter(value) if ',' in value else value.strip()
                excludes[key[8:]] = parsed_value
            else:
                parsed_value = parse_list_parameter(value) if ',' in value else value.strip()
                if parsed_value is not None:
                    filters[key] = parsed_value

        return filters, excludes

    def get_pagination_params(self, filters):
        top = int(filters.pop('top', 0))
        bottom = filters.pop('bottom', None)
        if bottom:
            bottom = int(bottom)
        else:
            bottom = top + self.size_per_request
        return top, bottom

    def filter_queryset(self, filters, excludes):
        filter_q = Q(**filters)
        exclude_q = Q(**excludes)
        return self.queryset.filter(filter_q).exclude(exclude_q)

    def filter(self, request, filters, excludes, top, bottom):
        queryset = self.filter_queryset(filters, excludes)
        
        paginator = Paginator(queryset, self.size_per_request)
        page_number = (top // self.size_per_request) + 1
        page = paginator.get_page(page_number)
        
        serializer = self.serializer_class(page, many=True)
        data = {
            'objects': serializer.data,
            'total_count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': page.number
        }
        
        cache_key = self.get_list_cache_key(filters, excludes, top, bottom)
        cache.set(cache_key, data, self.cache_duration)
        
        return Response(data, status=status.HTTP_200_OK)

    def get_serialized_object(self, pk):
        instance = get_object_or_404(self.queryset, pk=pk)
        return self.serializer_class(instance).data