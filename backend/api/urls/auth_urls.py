from django.urls import path
from ..views import (
    register_client,
    register_barber,
    verify_client,
    get_user,
    login_user,
    logout_user,
    request_password_reset,
    confirm_password_reset,
    refresh_token
)

urlpatterns = [
    path('register/', register_client, name='register_client'),
    path('register/<uidb64>/<token>/', register_barber, name='register_barber'),
    path('verify/<uidb64>/<token>/', verify_client, name='verify_client_email'),
    
    path('me/', get_user, name='get_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    
    path('reset-password/', request_password_reset, name='request_password_reset'),
    path('reset-password/<uidb64>/<token>/', confirm_password_reset, name='confirm_password_reset' ),
    
    path('refresh-token/', refresh_token, name='refresh_token'),
]
