from django.urls import path
from ..views import (
    invite_barber,
    delete_barber,
    create_barber_availability,
    manage_barber_availability,
)

urlpatterns = [
    path('barbers/', invite_barber, name='invite_barber'),
    path('barbers/<int:barber_id>/', delete_barber, name='delete_barber'),
    path('barbers/<int:barber_id>/availabilities/', create_barber_availability, name='create_barber_availability'),
    path('barbers/<int:barber_id>/availabilities/<int:availability_id>/', manage_barber_availability, name='manage_barber_availability'),
]