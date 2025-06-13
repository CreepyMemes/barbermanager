from django.urls import path
from ..views import (
    get_barbers_list,
    get_barber_availabilities_public,
    get_barber_services_public,
    get_barber_profile,
)

urlpatterns = [
    # Barber getters
    path('barbers/', get_barbers_list, name='get_barbers_list'),
    path('barbers/<int:barber_id>/availabilities/', get_barber_availabilities_public, name='get_barber_availabilities_public'),
    path('barbers/<int:barber_id>/services/', get_barber_services_public, name='get_barber_services_public'),
    path('barbers/<int:barber_id>/profile/', get_barber_profile, name='get_barber_profile'),
]
