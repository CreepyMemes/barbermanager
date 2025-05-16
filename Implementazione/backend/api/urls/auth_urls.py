from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from ..views.auth import (
    register_client,
    login_user,
    logout_user,
    verify_email,
    register_barber,
    request_password_reset,
    confirm_password_reset,
    refresh_token
)

urlpatterns = [
    path('register/', register_client, name='register_client'),
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
    
    path('register-barber/<uidb64>/<token>/', register_barber, name='register_barber'),
    
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    
    path('reset-password/', request_password_reset, name='request_password_reset'),
    path('reset-password/<uidb64>/<token>/', confirm_password_reset, name='confirm_password_reset' ),
    
    path('refresh-token/', refresh_token, name='refresh_token'),
]
