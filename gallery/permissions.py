from rest_framework.permissions import BasePermission
from myauth.utils import get_user


class IsArtworkOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        user = get_user(request)
        return obj.artist.user.pk == user.pk


class IsBidOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        user = get_user(request)
        return obj.bidder.user.pk == user.pk
