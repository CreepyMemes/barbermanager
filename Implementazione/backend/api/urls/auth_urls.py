from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from ..views.auth import (
    register_client,
    login_user,
    verify_email,
    register_barber,
    request_password_reset,
    confirm_password_reset,
    refresh_token
)

urlpatterns = [
    path('register/', register_client),
    path('login/', login_user),
    path('verify-email/<uidb64>/<token>/', verify_email),
    path('register-barber/<uidb64>/<token>/', register_barber),
    path('reset-password/', request_password_reset),
    path('reset-password/<uidb64>/<token>/', confirm_password_reset),
    path('refresh-token/', refresh_token),
]
