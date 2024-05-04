from django.urls import path
from .views import Register, Login, UserView, Logout, EmailCheckerView

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', Logout.as_view()),
    path('check-email/', EmailCheckerView.as_view()),
]