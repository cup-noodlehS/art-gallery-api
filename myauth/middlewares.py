import jwt
from django.utils.functional import SimpleLazyObject
from django.contrib.auth import get_user_model


class JWTAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            token_header = request.headers.get('Authorization')
            if not token_header:
                return self.get_response(request)
            if 'Bearer ' in token_header:
                token = token_header.split('Bearer ')[1]

        try:
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return self.get_response(request)
        
        user_id = decoded.get('id')
        if user_id:
            User = get_user_model()
            request_user = User.objects.get(pk=user_id)
            # request.user = SimpleLazyObject(lambda: request_user) # i get CSRF Failed: CSRF cookie not set when i change the request.user, fix this

        response = self.get_response(request)
        return response
