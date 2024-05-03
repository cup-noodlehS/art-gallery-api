from django.urls import path
from .views import (ArtworkView, CategoryView, BidView, TopArtistsView,
                    TransactionView, FeaturedArtworkView)

urlpatterns = [
    path('artworks/', ArtworkView.as_view({'get': 'list', 'post': 'create'})),
    path('artworks/<int:pk>/', ArtworkView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('categories/', CategoryView.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:pk>/', CategoryView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('bids/', BidView.as_view({'get': 'list', 'post': 'create'})),
    path('bids/<int:pk>/', BidView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('top-artists/', TopArtistsView.as_view()),
    path('transactions/<int:thread_pk>/', TransactionView.as_view()),
    path('featured-artworks/', FeaturedArtworkView.as_view()),
]
