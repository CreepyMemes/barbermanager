from django.urls import path
from .views import invite_barber, register_barber

urlpatterns = [
    path('invite-barber/', invite_barber),
    path('register-barber/', register_barber),
]
