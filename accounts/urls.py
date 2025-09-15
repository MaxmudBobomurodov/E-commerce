from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

from accounts.views import RegisterAPIView, LoginAPIView, GetAccessToken, UserIsAuthenticated

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('refresh/',GetAccessToken.as_view()),
    path('profile/', UserIsAuthenticated.as_view()),
]