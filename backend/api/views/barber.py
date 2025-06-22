from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from ..utils import (
    IsBarberRole,
)
from ..serializers import (
    GetBarberProfileSerializer,
    UpdateBarberProfileSerializer,
    DeleteBarberProfileSerializer,
    GetBarberAvailabilitiesSerializer,
    GetBarberServicesSerializer,
    CreateBarberServiceSerializer,
    UpdateBarberServiceSerializer,
    DeleteBarberServiceSerializer,
    GeBarberAppointmentsSerializer,
    GetBarberReviewsSerializer,
)


@extend_schema(
    methods=['GET'],
    responses={200: GetBarberProfileSerializer},
    description="Barber only: Get all public information related to the authenticated barber's profile.",
)
@extend_schema(
    methods=['PATCH'],
    request=UpdateBarberProfileSerializer,
    responses={200: OpenApiResponse(description="Profile info updated successfully.")},
    description="Barber only: Update information for the authenticated barber's profile.",
)
@extend_schema(
    methods=['DELETE'],
    responses={204: OpenApiResponse(description="Barber deleted successfully.")},
    description="Barber only: Delete the authenticated barber's account.",
)
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsBarberRole])
@parser_classes([JSONParser]) 
def manage_barber_profile(request):
    """
    Barber only: Handles get and update operations for the authenticated barber's profile.

    - GET: Updates general profie information by the authenticated barber.
    - PATCH: Barber only: Gets all related profile information for authenticated barber.
    - DELETE: Deletes the account of the authenticated barber.
    """
    if request.method == 'GET':
        serializer = GetBarberProfileSerializer(data={}, context={'barber': request.user})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PATCH':
        serializer = UpdateBarberProfileSerializer(data=request.data, context={'barber': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"detail": "Profile info updated successfully."}, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        serializer = DeleteBarberProfileSerializer(data={}, context={'barber': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    responses={200: GetBarberAvailabilitiesSerializer},
    description="Barber only: Get all availabilities for the authenticated barber.",
)
@api_view(['GET'])
@permission_classes([IsBarberRole])
@parser_classes([JSONParser]) 
def get_barber_availabilities(request):
    """
    Barber only: Get all availabilities for the authenticated barber.
    """
    serializer = GetBarberAvailabilitiesSerializer(data={}, context={'barber': request.user})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    methods=['GET'],
    responses={200: GetBarberServicesSerializer},
    description="Barber only: List all services offered by the authenticated barber.",
)
@extend_schema(
    methods=['POST'],
    request=CreateBarberServiceSerializer,
    responses={201: OpenApiResponse(description="Service added successfully.")},
    description="Barber only: Create a new service offering for the authenticated barber.",
)
@api_view(['GET', 'POST'])
@permission_classes([IsBarberRole])
@parser_classes([JSONParser]) 
def manage_barber_services(request):
    """
    Barber only: Handles get and create operations for services offered by the authenticated barber.

    - GET: Gets all services offered by the authenticated barber.
    - POST: Creates a new service offering for the authenticated barber.
    """
    if request.method == 'GET':
        serializer = GetBarberServicesSerializer(data={}, context={'barber': request.user})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CreateBarberServiceSerializer(data=request.data, context={'barber': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Service added successfully.'}, status=status.HTTP_201_CREATED)


@extend_schema(
    methods=['PATCH'],
    request=UpdateBarberServiceSerializer,
    responses={200: OpenApiResponse(description="Service updated successfully.")},
    description="Barber only: Edit the details (name/price) of a given service.",
)
@extend_schema(
    methods=['DELETE'],
    responses={204: OpenApiResponse(description="Service deleted successfully.")},
    description="Barber only: Delete a given service.",
)
@api_view(['PATCH', 'DELETE'])
@permission_classes([IsBarberRole])
@parser_classes([JSONParser]) 
def manage_barber_service(request, service_id):
    """
    Barber only: Handles update and delete operations for a specific service by the authenticated barber.

    - PATCH: Edit the details (name/price) of a given service.
    - DELETE: Remove a given service.
    """
    if request.method == 'PATCH':
        serializer = UpdateBarberServiceSerializer(data=request.data, context={'barber': request.user, 'service_id': service_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"detail": "Service updated successfully."}, status=status.HTTP_200_OK)
    

    elif request.method == 'DELETE':
        serializer = DeleteBarberServiceSerializer(data={}, context={'barber': request.user, 'service_id': service_id})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@extend_schema(
    responses={200: GeBarberAppointmentsSerializer},
    description="Barber only: Get all ONGOING appointments for the authenticated barber.",
)
@api_view(['GET'])
@permission_classes([IsBarberRole])
@parser_classes([JSONParser]) 
def get_barber_appointments(request):
    """
    Barber only: Get all appointments for the authenticated barber.
    """
    serializer = GeBarberAppointmentsSerializer(data={}, context={'barber': request.user})
    serializer.is_valid(raise_exception=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: GetBarberReviewsSerializer},
    description="Barber only: Get all reviews received by the authenticated barber.",
)
@api_view(['GET'])
@permission_classes([IsBarberRole])
@parser_classes([JSONParser]) 
def get_barber_reviews(request):
    """
    Barber only: Get all reviews received by the authenticated barber.
    """
    serializer = GetBarberReviewsSerializer(data={}, context={'barber': request.user})
    serializer.is_valid(raise_exception=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
