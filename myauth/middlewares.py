import jwt
from django.conf import settings
from .models import User
from rest_framework.authentication import BaseAuthentication


class JWTAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            token_header = request.headers.get('Authorization')
            if 'Bearer ' in token_header:
                token = token_header.split('Bearer ')[1]

        if token:
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded.get('id')
            if user_id:
                user = User.objects.filter(id=user_id).first()
                request.user = user

        response = self.get_response(request)
        return response
