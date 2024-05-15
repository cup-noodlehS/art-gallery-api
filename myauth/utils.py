from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
import jwt
from myauth.models import User


def get_user(request):
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
    return user