from django.urls import path
from .views import (
    CustomRegisterView,
    CustomLoginView,
    confirm_email,
    invite_barber, 
    register_barber, 
    request_password_reset, 
    confirm_password_reset
)

urlpatterns = [
    path('auth/register/', CustomRegisterView.as_view(), name='custom_register'),
    path('auth/login/', CustomLoginView.as_view(), name='custom_login'),
    path('confirm-email/<uidb64>/<token>/', confirm_email),
    path('invite-barber/', invite_barber),
    path('register-barber/<uidb64>/<token>/', register_barber),
    path('reset-password/', request_password_reset),
    path('reset-password/<uidb64>/<token>/', confirm_password_reset),
]
