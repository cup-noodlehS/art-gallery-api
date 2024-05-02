from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction

from gallery.models import Message, MessageThread, Artwork
from myauth.models import User
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
    

class TransactionView(APIView):
    def post(self, request):
        artist = request.user
        buyer = get_object_or_404(User, pk=request.data.get('buyer_id'))
        artwork_pk = request.data.get('artwork_id')
        if artwork_pk is None or buyer is None or artist is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            artwork = get_object_or_404(Artwork, pk=artwork_pk)
            artwork.status = Artwork.RESERVED
            artwork.buyer = buyer
            artwork.save(update_fields=['status', 'buyer'])

            message_thread = MessageThread.objects.create(artwork=artwork, artist=artist, buyer=buyer)
            Message.objects.create(thread=message_thread, sender=artist, message=f'{artwork_pk} is now reserved for {buyer.username}')
            object = MessageThreadSerializer(message_thread)
            return Response(object.data, status=status.HTTP_201_CREATED)
        
    def delete(self, request, thread_pk=None):
        if thread_pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            thread = get_object_or_404(MessageThread, pk=thread_pk)
            artwork = get_object_or_404(Artwork, pk=thread.artwork.pk)
            artwork.status = Artwork.OPEN
            artwork.buyer = None
            artwork.save(update_fields=['status', 'buyer'])
            thread.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)