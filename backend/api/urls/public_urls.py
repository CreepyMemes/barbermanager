from django.urls import path
from ..views import (
    get_barbers_list,
    get_barber_availability,
)

urlpatterns = [
    path('barber/', get_barbers_list, name='get_barbers_list'),
    path('barber/<int:barber_id>/availability/', get_barber_availability, name='get_barber_availability'),
]
