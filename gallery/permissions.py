from rest_framework.permissions import BasePermission


class IsArtworkOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # return obj.artist.user == request.user
        return True
    

class IsBidOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # return obj.bidder.user == request.user
        return True