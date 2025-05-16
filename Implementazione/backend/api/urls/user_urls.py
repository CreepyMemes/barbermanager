from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from ..views.user import (
    invite_barber,
    get_user,
)

urlpatterns = [
    path('invite-barber/', invite_barber, name='invite_barber'),
    path('me/', get_user, name='get_user'),
]
