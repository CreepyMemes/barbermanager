from django.urls import path
from ..views import (
    get_barber_availabilities,
    manage_barber_services,
    manage_barber_service,
    get_barber_appointments,
    get_barber_reviews,
)


urlpatterns = [
    # Service management
    path('services/', manage_barber_services, name='get_barber_services'),
    path('services/<int:service_id>/', manage_barber_service, name='manage_barber_service'),

    # Getters for authenticated barber
    path('availabilities/', get_barber_availabilities, name='get_barber_availabilities'),
    path('appointments/', get_barber_appointments, name='get_barber_appointments'),
    path('reviews/', get_barber_reviews, name='get_barber_reviews'),
]