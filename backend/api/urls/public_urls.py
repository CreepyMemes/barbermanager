from django.urls import path
from ..views import (
    get_barbers_list,
    get_barber_availability,
    get_barber_services,
)

urlpatterns = [
    path('barber/', get_barbers_list, name='get_barbers_list'),
    path('barber/<int:barber_id>/availability/', get_barber_availability, name='get_barber_availability'),
    path('barber/<int:barber_id>/services/', get_barber_services, name='get_barber_services'),
]
