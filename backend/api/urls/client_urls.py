from django.urls import path
from ..views.client import (
    get_client_appointments,
    delete_client_appointment,
    get_client_reviews,
    create_client_review,
    edit_client_review,
    delete_client_review,
)

urlpatterns = [
    # Appointments
    path('appointments/', get_client_appointments, name='get_client_appointments'),
    path('appointment/<int:appointment_id>/', delete_client_appointment, name='delete_client_appointment'),

    # Reviews
    path('reviews/', get_client_reviews, name='get_client_reviews'),
    path('review/<int:appointment_id>/', create_client_review, name='create_client_review'),
    path('review/<int:review_id>/', edit_client_review, name='edit_client_review'),
    path('review/<int:review_id>/', delete_client_review, name='delete_client_review'),
]
