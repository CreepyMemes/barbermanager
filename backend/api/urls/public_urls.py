from django.urls import path
from ..views import (
    get_barbers_public,
    get_barber_availabilities_public,
    get_barber_slots_public,
    get_barber_services_public,
    get_barber_profile_public,
    get_client_profile_public,
)

urlpatterns = [
    # Barber getters
    path('barbers/', get_barbers_public, name='get_barbers_list'),
    path('barbers/<int:barber_id>/profile/', get_barber_profile_public, name='get_barber_profile_public'),
    path('clients/<int:client_id>/profile/', get_client_profile_public, name='get_client_profile_public'),
    path('barbers/<int:barber_id>/availabilities/', get_barber_availabilities_public, name='get_barber_availabilities_public'),
    path('barbers/<int:barber_id>/slots/', get_barber_slots_public, name='get_barber_slots_public'),
    path('barbers/<int:barber_id>/services/', get_barber_services_public, name='get_barber_services_public'),
]
