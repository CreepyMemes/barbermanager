from django.urls import path
from ..views import (
    manage_profile_image,
)

urlpatterns = [
    path('profile/', manage_profile_image, name='manage_profile_image'),
]