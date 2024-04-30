from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from gallery.models import Message, MessageThread
from gallery.serializers import MessageThreadSerializer, MessageSerializer




class MessagesView(APIView):
    def get(self, request):
        queryset = MessageThread.objects.all()
        filters = {}
        for key in request.query_params.keys():
            filters[key] = request.query_params[key]
        
        if filters:
            queryset = queryset.filter(**filters)
        
        serializer = MessageThreadSerializer(queryset, many=True)
        return Response(serializer.data)


class MessageThreadView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        queryset = MessageThread.objects.all()
        message_thread = get_object_or_404(queryset, pk=pk)
        serializer = MessageThreadSerializer(message_thread)
        return Response(serializer.data)


class MessageView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Message.objects.all()
        message = get_object_or_404(queryset, pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)