from django.urls import path
from ..views.client import (
    get_client_appointments,
    create_client_appointment,
    cancel_client_appointment,
    get_client_reviews,
    create_client_review,
    edit_client_review,
    delete_client_review,
)

urlpatterns = [
    path('appointments/', get_client_appointments, name='get_client_appointments'),
    path('appointments/barbers/<int:barber_id>/', create_client_appointment, name='create_client_appointment'),
    path('appointments/<int:appointment_id>/', cancel_client_appointment, name='delete_client_appointment'),

    # TODO: Reviews
    path('reviews/', get_client_reviews, name='get_client_reviews'),
    path('reviews/<int:appointment_id>/', create_client_review, name='create_client_review'),
    path('reviews/<int:review_id>/', edit_client_review, name='edit_client_review'),
    path('reviews/<int:review_id>/', delete_client_review, name='delete_client_review'),
]
