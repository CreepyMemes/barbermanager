from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from ..views.user import (
    get_user,
    invite_barber,
)

urlpatterns = [
    path('invite-barber/', invite_barber),
    path('me/', get_user, name='get_user'),
]
