from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from ..views.auth import (
    register_client,
    login_user,
    confirm_email,
    register_barber,
    confirm_password_reset
)

urlpatterns = [
    path('register/', register_client),
    path('login/', login_user),
    path('confirm-email/<uidb64>/<token>/', confirm_email),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-barber/<uidb64>/<token>/', register_barber),
    
    path('reset-password/<uidb64>/<token>/', confirm_password_reset),
]
