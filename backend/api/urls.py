from django.urls import path
from .views import invite_barber

urlpatterns = [
    path('invite-barber/', invite_barber),
]
