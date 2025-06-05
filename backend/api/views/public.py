from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..serializers import (
    GetBarberListSerializer,
    GetBarberAvailabilitiesSerializer,
    GetBarberServicesSerializer,
)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def get_barbers_list(request):
    """
    Return a list of all active barbers
    """
    serializer = GetBarberListSerializer(instance={}) 
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def get_barber_availabilities_public(request, barber_id):
    """
    Get all availabilities for a specific barber.
    """
    serializer = GetBarberAvailabilitiesSerializer(data={}, context={'barber_id': barber_id})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def get_barber_services_public(request, barber_id):
    """
    Get all services for the given barber.
    """
    serializer = GetBarberServicesSerializer(data={}, context={'barber_id': barber_id})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)