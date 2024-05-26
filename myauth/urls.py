from django.urls import path
from .views import Register, Login, UserView, Logout, EmailCheckerView, GalleryUsers, LocationView

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', Logout.as_view()),
    path('check-email/', EmailCheckerView.as_view()),
    path('gallery-user/', GalleryUsers.as_view({'get':'list'})),
    path('gallery-user/<int:pk>/', GalleryUsers.as_view({'get':'retrieve'})),
    path('user-location/', LocationView.as_view())
]