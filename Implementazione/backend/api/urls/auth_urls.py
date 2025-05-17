from django.urls import path
from ..views.auth import (
    register_client,
    verify_client,
    register_barber,
    login_user,
    logout_user,
    request_password_reset,
    confirm_password_reset,
    refresh_token
)

urlpatterns = [
    path('register-client/', register_client, name='register_client'),
    path('verify-client/<uidb64>/<token>/', verify_client, name='verify_client'),
    path('register-barber/<uidb64>/<token>/', register_barber, name='register_barber'),
    
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    
    path('request-password-reset/', request_password_reset, name='request_password_reset'),
    path('reset-password/<uidb64>/<token>/', confirm_password_reset, name='confirm_password_reset' ),
    
    path('refresh-token/', refresh_token, name='refresh_token'),
]
