from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .consumers import MyConsumer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('gallery.urls')),
]

websocket_urlpatterns = [
    path('ws/myapp/', MyConsumer.as_asgi()),
]
