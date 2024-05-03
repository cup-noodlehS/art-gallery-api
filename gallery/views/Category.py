from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.shortcuts import get_object_or_404

from gallery.models import Category
from gallery.serializers import CategorySerializer


class CategoryView(viewsets.ViewSet):
    def list(self, request):
        queryset = Category.objects.all()

        filters = {}
        for key in request.query_params.keys():
            filters[key] = request.query_params[key]

        top = filters.pop('top', 0)
        bottom = filters.pop('bottom', None)
        if top != 0:
            top = int(top)
        if bottom is not None:
            bottom = int(bottom)

        size_per_request = 20
        if bottom is None:
            bottom = top + size_per_request

        if filters:
            queryset = queryset.filter(**filters)

        serializer = CategorySerializer(queryset, many=True)
        total_count = len(serializer.data)
        objects = serializer.data[top:bottom]
        return Response({
            'total_count': total_count,
            'objects': objects,
        })

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