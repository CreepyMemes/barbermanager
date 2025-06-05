from django.urls import path
from ..views import (
    manage_services,
    get_upcoming_appointments,
)

urlpatterns = [
    path('service/', manage_services, name='manage_services'),
    path('appointments/', get_upcoming_appointments, name='get_upcoming_appointments'),
]
