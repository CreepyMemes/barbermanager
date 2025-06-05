from django.urls import path
from ..views import (
    add_service,
    manage_service
)

urlpatterns = [
    path('service/', add_service, name='add_service'),
    path('service/<int:service_id>/', manage_service, name='manage_service')
]
