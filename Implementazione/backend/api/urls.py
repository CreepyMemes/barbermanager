from django.urls import path
from .views import (
    invite_barber, 
    register_barber, 
    request_password_reset, 
    confirm_password_reset
)

urlpatterns = [
    path('invite-barber/', invite_barber),
    path('register-barber/<uidb64>/<token>/', register_barber),
    path('reset-password/', request_password_reset),
    path('reset-password/<uidb64>/<token>/', confirm_password_reset),
]
