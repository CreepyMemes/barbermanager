from django.urls import path
from ..views import (
    get_admin_profile,
    invite_barber,
    delete_barber,
    create_barber_availability,
    manage_barber_availability,
    get_admin_statistics,
    get_all_appointments,
)

urlpatterns = [
    # Barber User management
    path('barbers/', invite_barber, name='invite_barber'),
    path('barbers/<int:barber_id>/', delete_barber, name='delete_barber'),

    # Barber Availability management
    path('barbers/<int:barber_id>/availabilities/', create_barber_availability, name='create_barber_availability'),
    path('barbers/<int:barber_id>/availabilities/<int:availability_id>/', manage_barber_availability, name='manage_barber_availability'),

    # Appointments
    path('appointments/', get_all_appointments, name='get_all_appointments'),
    
    # Statistics 
    path('statistics/', get_admin_statistics, name='get_admin_statistics'),

    # Getters for authenticated admin
    path('profile/', get_admin_profile, name='get_admin_profile'),
]