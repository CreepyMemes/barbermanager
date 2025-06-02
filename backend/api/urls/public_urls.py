from django.urls import path
from ..views.public import get_barber_public_availability
from ..views.public import (
    get_barbers_list,
)

urlpatterns = [
    path('barber/', get_barbers_list, name='get_barbers_list'),
    path('barber/<int:barber_id>/availability/', get_barber_public_availability, name='barber_public_availability'),
]
