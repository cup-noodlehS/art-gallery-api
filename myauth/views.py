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

from .models import User
from .serializers import UserSerializer
from faso.utils import upload_to_cloudinary


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        token_header = request.headers.get('Authorization')

        if not token and not token_header:
            raise AuthenticationFailed('Unauthenticated!')
        
        if not token and token_header:
            if 'Bearer ' not in token_header:
                raise AuthenticationFailed('Invalid token format')
            token = token_header.split('Bearer ')[1]
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = get_object_or_404(User, id=payload['id'])

        if datetime.datetime.now() + datetime.timedelta(days=2) > datetime.datetime.fromtimestamp(payload['exp']):
            payload['exp'] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)

        return Response(UserSerializer(user).data)


class Register(APIView):
    def post(self, request):
        data = request.data.copy()
        avatar_files = data.pop('avatar_file', None)
        if avatar_files is not None:
            try:
                data['avatar_url'] = upload_to_cloudinary(avatar_files, 'pfp')
            except:
                return Response({'error': 'Error uploading image'}, status=status.HTTP_400_BAD_REQUEST)
            
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
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
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
