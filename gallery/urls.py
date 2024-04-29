from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import ArtworkView, CategoryView, BidView

urlpatterns = [
    path('artworks/', ArtworkView.as_view({'get': 'list', 'post': 'create'})),
    path('artworks/<int:pk>/', ArtworkView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('categories/', CategoryView.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:pk>/', CategoryView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('bids/', BidView.as_view({'get': 'list', 'post': 'create'})),
    path('bids/<int:pk>/', BidView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
