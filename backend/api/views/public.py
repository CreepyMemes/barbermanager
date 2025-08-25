from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from ..serializers import (
    GetBarbersPublicSerializer,
    GetBarberAvailabilitiesSerializer,
    GetBarberSlotsSerializer,
    GetBarberServicesSerializer,
    GetBarberProfilePublicSerializer,
    GetClientProfilePublicSerializer
)


@extend_schema(
    responses={200: GetBarbersPublicSerializer},
    description="Return a list of all active barbers.",
)
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
@parser_classes([JSONParser]) 
def get_barbers_public(request):
    """
    Return a list of all active barbers
    """
    serializer = GetBarbersPublicSerializer(data={}, instance={}) 
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: GetBarberProfilePublicSerializer},
    description="Get all public profile information for a barber. (Public)",
)
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
@parser_classes([JSONParser]) 
def get_barber_profile_public(request, barber_id):
    """
    Get all services for the given barber.
    """
    serializer = GetBarberProfilePublicSerializer(data={}, context={'barber_id': barber_id})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: GetClientProfilePublicSerializer},
    description="Get all public profile information for a client. (Public)",
)
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
@parser_classes([JSONParser]) 
def get_client_profile_public(request, client_id):
    """
    Get all services for the given client.
    """
    serializer = GetClientProfilePublicSerializer(data={}, context={'client_id': client_id})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: GetBarberAvailabilitiesSerializer},
    description="Get all availabilities for a specific barber. (Public)",
)
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
@parser_classes([JSONParser]) 
def get_barber_availabilities_public(request, barber_id):
    """
    Get all availabilities for a specific barber.
    """
    serializer = GetBarberAvailabilitiesSerializer(data={}, context={'barber_id': barber_id})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    methods=['POST'],
    request=GetBarberSlotsSerializer,
    responses={2010: OpenApiResponse(description="Returns the time slots for the selected date")},
    description="Get all slots for a barber on a given date. (Public)"
)
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
@parser_classes([JSONParser])
def get_barber_slots_public(request, barber_id):
    """
    Get all slots for a given barber and date (date in JSON).
    """
    serializer = GetBarberSlotsSerializer(data=request.data, context={'barber_id': barber_id})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: GetBarberServicesSerializer},
    description="Get all services for the given barber. (Public)",
)
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
@parser_classes([JSONParser]) 
def get_barber_services_public(request, barber_id):
    """
    Get all services for the given barber.
    """
    serializer = GetBarberServicesSerializer(data={}, context={'barber_id': barber_id})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)