from django.urls import path
from ..views.public import (
    get_barbers_list,
)

urlpatterns = [
    path('barber/', get_barbers_list, name='get_barbers_list'),
]
