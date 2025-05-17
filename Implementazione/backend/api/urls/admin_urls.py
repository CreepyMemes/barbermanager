from django.urls import path
from ..views.admin import (
    invite_barber,
)

urlpatterns = [
    path('invite-barber/', invite_barber, name='invite_barber'),
]
