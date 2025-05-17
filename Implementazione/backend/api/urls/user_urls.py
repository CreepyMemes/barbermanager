from django.urls import path
from ..views.user import (
    get_user,
)

urlpatterns = [
    path('me/', get_user, name='get_user'),
]
