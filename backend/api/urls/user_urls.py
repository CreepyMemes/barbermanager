from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from ..views.user import (
    invite_barber,
    request_password_reset,
    get_user,
)

urlpatterns = [
    path('invite-barber/', invite_barber),
    path('reset-password/', request_password_reset),
    path('me/', get_user, name='get_user'),
]
