from django.shortcuts import render
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
import jwt, datetime
import cloudinary
from cloudinary.uploader import upload

from .models import User, UserLocation
from .serializers import UserSerializer, UserLocationSerializer
from faso.utils import upload_to_cloudinary
from myauth.utils import get_user


class UserView(APIView):
    def get(self, request):
        user = get_user(request)
        if user.is_banned:
            return Response({'error': 'User is banned'}, status=status.HTTP_403_FORBIDDEN)
        return Response(UserSerializer(user).data)


class Register(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            print(e.detail)
            return Response({'error': 'Validation Error'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    

class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('Incorrect email or password')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect email or password')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365),
            'iat': datetime.datetime.now(datetime.timezone.utc)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'user': UserSerializer(user).data
        }
        
        return response
    

class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class EmailCheckerView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            return Response({'is_available': False})
        return Response({'is_available': True})
    

class GalleryUsers(viewsets.ViewSet):
    def list(self, request):
        query_set = User.objects.all()
        filters = {}
        for key in request.query_params.keys():
            filters[key] = request.query_params[key]
        
        top = filters.pop('top', 0)
        size_per_request = 20
        if filters:
            query_set = query_set.filter(*filters)

        objects = UserSerializer(query_set, many=True).data
        total_count = len(objects)
        objects = objects[top:top + size_per_request]

        return Response({
            'total_count': total_count,
            'objects': objects
        })
    
    def retrieve(self, request, pk=None):
        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        object = User.objects.get(pk=pk)
        serialized = UserSerializer(object)
        return Response(serialized.data)
    

class LocationView(APIView):
    def get(self, request):
        query_set = UserLocation.objects.all()
        filters = {}
        for key in request.query_params.keys():
            filters[key] = request.query_params[key]
        top = filters.pop('top', 0)
        size_per_request = 20
        if filters:
            query_set = query_set.filter(*filters)
        
        objects = UserLocationSerializer(query_set, many=True).data
        total_count = len(objects)
        objects = objects[top:top + size_per_request]

        return Response({
            'total_count': total_count,
            'objects': objects
        })
    
    def post(self, request):
        name = request.data.get('name')
        existing = UserLocation.objects.filter(name=name).first()
        if existing:
            object = UserLocationSerializer(existing)
            return Response(object.data)
        
        serializer = UserLocationSerializer(data={'name': name})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
