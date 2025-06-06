from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..utils import (
    IsBarberRole,
)
from ..serializers import (
    GetBarberAvailabilitiesSerializer,
    GetBarberServicesSerializer,
    CreateBarberServiceSerializer,
    UpdateBarberServiceSerializer,
    DeleteBarberServiceSerializer,
    GeBarberAppointmentsSerializer,
)


@api_view(['GET'])
@permission_classes([IsBarberRole])
def get_barber_availabilities(request):
    """
    Get all availabilities for the authenticated barber.
    """
    serializer = GetBarberAvailabilitiesSerializer(data={}, context={'barber_id': request.user})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsBarberRole])
def get_barber_services(request):
    """
    Get all services offered by the authenticated barber.
    """
    serializer = GetBarberServicesSerializer(data={}, context={'barber_id': request.user})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsBarberRole])
def create_barber_service(request):
    """
    Barber only: Creates a new service offering for the authenticated barber.
    """
    serializer = CreateBarberServiceSerializer(data=request.data, context={'barber_id': request.user})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({'detail': 'Service added successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsBarberRole])
def manage_barber_service(request, service_id):
    """
    Barber only: Handles update and delete operations for a specific service by the authenticated barber.

    - PATCH: Edit the details (name/price) of a given service.
    - DELETE: Remove a given service.
    """
    if request.method == 'PATCH':
        serializer = UpdateBarberServiceSerializer(data=request.data, context={'barber_id': request.user, 'service_id': service_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"detail": "Service updated successfully."}, status=status.HTTP_200_OK)
    

    elif request.method == 'DELETE':
        serializer = DeleteBarberServiceSerializer(data={}, context={'barber_id': request.user, 'service_id': service_id})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        
        return Response({"detail": "Service deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
@permission_classes([IsBarberRole])
def get_barber_appointments(request):
    """
    Get all appointments for the authenticated barber.
    """
    serializer = GeBarberAppointmentsSerializer(data={}, context={'barber_id': request.user})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

