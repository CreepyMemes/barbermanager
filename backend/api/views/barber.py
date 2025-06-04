from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..utils import (
    IsBarberRole,
)
from ..serializers import (
    ServiceSerializer,
)
from ..models import Service
from django.utils import timezone
from ..models import Appointment
from ..serializers import AppointmentSerializer
from ..models.appointment import AppointmentStatus
from datetime import date
from ..models import Barber

@api_view(['POST'])
@permission_classes([IsBarberRole])
def add_service(request):
    """
    Barber only: Adds a new service to the authenticated Barber
    """
    barber = request.user.barber  

    serializer = ServiceSerializer(data=request.data, context={'barber': barber})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({'detail': 'Service added successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['PATCH', 'DELETE'])
@permission_classes([IsBarberRole])
def update_or_delete_service(request, service_id):
    barber = request.user.barber
    service = get_object_or_404(Service, id=service_id, barber=barber)

    if request.method == 'PATCH':
        serializer = ServiceSerializer(service, data=request.data, partial=True, context={'barber': barber})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Service updated successfully.'})
    
    elif request.method == 'DELETE':
        service.delete()
        return Response({'detail': 'Service deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsBarberRole])
def get_upcoming_appointments(request):
    today = date.today()
    print(f"User: {request.user}")
    print(f"Today: {today}")

    appointments = Appointment.objects.filter(
        barber=request.user,
        date__gte=today,
        status=AppointmentStatus.ONGOING.value
    ).order_by('date', 'slot')

    print(f"Appointments found: {appointments.count()}")
    for app in appointments:
        print(f"Appointment: {app.id}, date: {app.date}, status: {app.status}")

    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)