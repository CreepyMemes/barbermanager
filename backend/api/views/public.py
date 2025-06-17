from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..serializers import (
    GetBarberListSerializer,
    GetBarberAvailabilitiesSerializer,
    GetBarberServicesSerializer,
    GetBarberProfileSerializer,
)


@extend_schema(
    responses={200: GetBarberListSerializer},
    description="Return a list of all active barbers.",
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


@extend_schema(
    responses={200: GetBarberProfileSerializer},
    description="Get all public profile information for a barber. (Public)",
)
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def get_barber_profile_public(request, barber_id):
    """
    Get all services for the given barber.
    """
    serializer = GetBarberProfileSerializer(data={}, context={'barber_id': barber_id})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: GetBarberAvailabilitiesSerializer},
    description="Get all availabilities for a specific barber. (Public)",
)
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


@extend_schema(
    responses={200: GetBarberServicesSerializer},
    description="Get all services for the given barber. (Public)",
)
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