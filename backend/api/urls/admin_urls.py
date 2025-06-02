from django.urls import path
from ..views.admin import (
    invite_barber,
    delete_barber,
    manage_barber_availability,  # nuova view unica
    get_barber_availability,
)

urlpatterns = [
    path('barber/', invite_barber, name='invite_barber'),
    path('barber/<int:barber_id>/', delete_barber, name='delete_barber'),
    path('availability/<int:barber_id>/', manage_barber_availability, name='manage_barber_availability'),  # POST, PATCH, DELETE tutti qui
    path('barber/<int:barber_id>/availability/<str:date>/', get_barber_availability, name='get_barber_availability'),  # GET per data specifica
]