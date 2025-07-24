from django.urls import path
from ..views import (
    manage_admin_profile,
    get_all_barbers,
    get_all_clients,
    invite_barber,
    delete_barber,
    create_barber_availability,
    manage_barber_availability,
    get_all_appointments,
)

urlpatterns = [
    # Admin profile management
    path('profile/', manage_admin_profile, name='manage_admin_profile'),

    # Barber User management
    path('barbers/invite/', invite_barber, name='invite_barber'),
    path('barbers/<int:barber_id>/', delete_barber, name='delete_barber'),

    # Barber Availability management
    path('barbers/<int:barber_id>/availabilities/', create_barber_availability, name='create_barber_availability'),
    path('barbers/<int:barber_id>/availabilities/<int:availability_id>/', manage_barber_availability, name='manage_barber_availability'),

    # Getters for authenticated admin
    path('barbers/', get_all_barbers, name='get_all_barbers'),
    path('clients/', get_all_clients, name='get_all_clients'),
    path('appointments/', get_all_appointments, name='get_all_appointments'),
]