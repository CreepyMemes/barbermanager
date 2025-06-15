from django.urls import path
from ..views.client import (
    get_client_profile,
    get_client_appointments,
    create_client_appointment,
    cancel_client_appointment,
    get_client_reviews,
    create_client_review,
    manage_client_reviews,
)

urlpatterns = [
    # Appointment management
    path('appointments/', get_client_appointments, name='get_client_appointments'),
    path('appointments/barbers/<int:barber_id>/', create_client_appointment, name='create_client_appointment'),
    path('appointments/<int:appointment_id>/', cancel_client_appointment, name='delete_client_appointment'),

    # Review management
    path('reviews/', get_client_reviews, name='get_client_reviews'),
    path('reviews/appointments/<int:appointment_id>/', create_client_review, name='create_client_review'),
    path('reviews/<int:review_id>/', manage_client_reviews, name='manage_client_reviews'),

    # Getters for authenticated client
    path('profile/', get_client_profile, name='get_client_profile'),
]
