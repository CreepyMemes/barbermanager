from django.urls import path
from ..views import (
    invite_barber,
    delete_barber,
    create_barber_availability,
    manage_barber_availability,
    get_admin_statistics,
)

urlpatterns = [
    path('barber/', invite_barber, name='invite_barber'),
    path('barber/<int:barber_id>/', delete_barber, name='delete_barber'),
    path('barber/<int:barber_id>/availability/', create_barber_availability, name='create_barber_availability'),
    path('barber/<int:barber_id>/availability/<availability_id>/', manage_barber_availability, name='manage_barber_availability'),
    path('admin/statistics/', get_admin_statistics),
]