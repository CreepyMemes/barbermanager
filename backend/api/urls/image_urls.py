from django.urls import path
from ..views import (
    manage_profile_picture,
)


urlpatterns = [
    path('profile/', manage_profile_picture, name='manage_profile_picture'),
]