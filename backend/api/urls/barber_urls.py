from django.urls import path
from ..views import (
    get_barber_availabilities,
    get_barber_services,
    create_barber_service,
    manage_barber_service,
    get_barber_appointments,
)


urlpatterns = [
    path('availabilities/', get_barber_availabilities, name='get_barber_availabilities'),
    path('services/', get_barber_services, name='get_barber_services'),
    path('service/', create_barber_service, name='create_barber_service'),
    path('service/<int:service_id>/', manage_barber_service, name='manage_barber_service'),

    # TODO
    path('appointments/', get_barber_appointments, name='get_barber_appointments'),
]