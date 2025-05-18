from django.urls import path
from ..views.admin import (
    invite_barber,
    delete_barber,
)

urlpatterns = [
    path('barber/', invite_barber, name='invite_barber'),
    path('barber/<int:barber_id>/', delete_barber, name='delete_barber')
]
