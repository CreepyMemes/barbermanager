from django.urls import path
from ..views import (
    add_service,
)

urlpatterns = [
    path('service/', add_service, name='add_service'),
]
