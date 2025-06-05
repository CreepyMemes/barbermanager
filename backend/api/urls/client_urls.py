from django.urls import path
from ..views.client import (
    client_appointments_list_create,
    client_appointment_delete,
    client_reviews_list,
    client_review_create,
    client_review_edit,
    client_review_delete,
)

urlpatterns = [
    # Appointments
    path('appointments/', client_appointments_list_create, name='client-appointments-list-create'),
    path('appointments/<int:appointment_id>/', client_appointment_delete, name='client-appointment-delete'),

    # Reviews
    path('reviews/', client_reviews_list, name='client-reviews-list'),
    path('reviews/<int:appointment_id>/', client_review_create, name='client-review-create'),
    path('reviews/<int:review_id>/', client_review_edit, name='client-review-edit'),
    path('reviews/<int:review_id>/', client_review_delete, name='client-review-delete'),
]
