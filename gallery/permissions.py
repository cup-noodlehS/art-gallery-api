from rest_framework.permissions import BasePermission


class IsArtworkOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.artist.user == request.user


class IsBidOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.bidder.user == request.user
