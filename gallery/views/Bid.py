from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.shortcuts import get_object_or_404

from gallery.models import Artwork, Bid
from gallery.serializers import BidSerializer
from gallery.permissions import IsBidOwner


class BidView(viewsets.ViewSet):
    permission_classes = [IsBidOwner]
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