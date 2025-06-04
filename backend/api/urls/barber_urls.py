from django.urls import path
from ..views import barber as views

urlpatterns = [
    path('service/', views.add_service),
    path('service/<int:service_id>/', views.update_or_delete_service), 
    path('appointments/', views.get_upcoming_appointments),
]
