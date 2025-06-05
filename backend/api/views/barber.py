from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..utils import (
    IsBarberRole,
)
from ..serializers import (
    CreateServiceSerializer,
    UpdateServiceSerializer,
    DeleteServiceSerializer,
    AppointmentSerializer,
)
from ..models import ( # TODO: move these to serializers (logic and validations shouldn't be in views)
    Appointment,
    AppointmentStatus,
)
from datetime import date


@api_view(['POST', 'PATCH', 'DELETE'])
@permission_classes([IsBarberRole])
def manage_services(request):
    """
    Admin only: Manages a barber's availability with (CREATE, UPDATE, DELETE operations).
    """
    if request.method == 'POST':
        serializer = CreateServiceSerializer(data=request.data, context={'barber_id': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Service added successfully.'}, status=status.HTTP_201_CREATED)
        
    elif request.method == 'PATCH': # if new fields are added to Service, set (partial=True)
        serializer = UpdateServiceSerializer(data=request.data, context={'barber_id': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"detail": "Service updated successfully."}, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        pass
        serializer = DeleteServiceSerializer(data=request.data, context={'barber_id': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        
        return Response({"detail": "Service deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

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