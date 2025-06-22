from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from ..utils import (
    IsClientRole,
)
from api.serializers.client import (
    GetClientProfileSerializer,
    UpdateClientProfileSerializer,
    DeleteClientProfileSerializer,
    GetClientAppointmentsSerializer,
    CreateClientAppointmentSerializer,
    CancelClientAppointmentSerializer,
    GetClientReviewsSerializer,
    CreateClientReviewSerializer,
    UpdateClientReviewSerializer,
    DeleteClientReviewSerializer,
)


@extend_schema(
    methods=["GET"],
    responses={200: GetClientProfileSerializer},
    description="Client only: Get all related profile information for the authenticated client.",
)
@extend_schema(
    methods=["PATCH"],
    request=UpdateClientProfileSerializer,
    responses={200: OpenApiResponse(description="Profile info updated successfully.")},
    description="Client only: Update general profile information (username, name, surname, phone_number) for the authenticated client.",
)
@extend_schema(
    methods=["DELETE"],
    responses={204: OpenApiResponse(description="Profile deleted successfully.")},
    description="Client only: Delete the account of the authenticated client.",
)
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsClientRole])
@parser_classes([JSONParser]) 
def manage_client_profile(request):
    """
    Client only: Handles get, update and delete operations for the authenticated clients's profile.

    - GET: Updates general profie information by the authenticated client.
    - PATCH: Gets all related profile information for authenticated client.
    - DELETE: Deletes the account of the authenticated client.
    """
    if request.method == 'GET':
        serializer = GetClientProfileSerializer(data={}, context={'client': request.user})
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PATCH':
        serializer = UpdateClientProfileSerializer(data=request.data, context={'client': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"detail": "Profile info updated successfully."}, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        serializer = DeleteClientProfileSerializer(data={}, context={'client': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@extend_schema(
    responses={200: GetClientAppointmentsSerializer},
    description="Client only: Get all appointments for the authenticated client.",
)
@api_view(['GET'])
@permission_classes([IsClientRole])
@parser_classes([JSONParser]) 
def get_client_appointments(request):
    """
    Client only: Get all appointments for the authenticated client.
    """
    serializer = GetClientAppointmentsSerializer(data={}, context={'client': request.user})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=CreateClientAppointmentSerializer,
    responses={201: OpenApiResponse(description="Appointment added successfully.")},
    description="Client only: Create an appointment for the authenticated client.",
)
@api_view(['POST'])
@permission_classes([IsClientRole])
@parser_classes([JSONParser]) 
def create_client_appointment(request, barber_id):
    """
    Client only: Creates an appointmentt for the authenticated client.
    """

    serializer = CreateClientAppointmentSerializer(data=request.data, context={'client': request.user, 'barber_id': barber_id})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({'detail': 'Appointment added successfully.'}, status=status.HTTP_201_CREATED)


@extend_schema(
    responses={200: OpenApiResponse(description="Appointment cancelled successfully.")},
    description="Client only: Cancel an ongoing appointment for the authenticated client.",
)
@api_view(['DELETE'])
@permission_classes([IsClientRole])
@parser_classes([JSONParser]) 
def cancel_client_appointment(request, appointment_id):
    """
    Client only: Cancels an ONGOING appointment by setting it's status to CANCELLED, for the authenticated client.
    """
    serializer = CancelClientAppointmentSerializer(data={}, context={'client': request.user, 'appointment_id': appointment_id})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({'detail': 'Appointment cancelled successfully.'}, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: GetClientReviewsSerializer},
    description="Client only: Get all reviews posted by the authenticated client.",
)
@api_view(['GET'])
@permission_classes([IsClientRole])
@parser_classes([JSONParser]) 
def get_client_reviews(request):
    """
    Get all reviews posted by the authenticated client.
    """
    serializer = GetClientReviewsSerializer(data={}, context={'client': request.user})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=CreateClientReviewSerializer,
    responses={201: OpenApiResponse(description="Review created successfully.")},
    description="Client only: Create a review for a completed appointment.",
)
@api_view(['POST'])
@permission_classes([IsClientRole])
@parser_classes([JSONParser]) 
def create_client_review(request, appointment_id):
    """
    Client only:  Creates a new review post for the barber associated to the authenticated client's appointment
    """
    serializer = CreateClientReviewSerializer(data=request.data,context={'client': request.user, 'appointment_id': appointment_id})
    serializer.is_valid(raise_exception=True)
    serializer.create(serializer.validated_data)

    return Response({'detail': 'Review created successfully.'}, status=status.HTTP_201_CREATED)


@extend_schema(
    methods=["PATCH"],
    request=UpdateClientReviewSerializer,
    responses={200: OpenApiResponse(description="Review updated successfully.")},
    description="Client only: Update a review by the authenticated client.",
)
@extend_schema(
    methods=["DELETE"],
    responses={204: OpenApiResponse(description="Review deleted successfully.")},
    description="Client only: Delete a review by the authenticated client.",
)
@api_view(['PATCH', 'DELETE'])
@permission_classes([IsClientRole])
@parser_classes([JSONParser]) 
def manage_client_reviews(request, review_id):
    """
    Edit or delete a review by the authenticated client.
    PATCH: Update rating or comment.
    DELETE: Remove the review.
    """
    if request.method == 'PATCH':
        serializer = UpdateClientReviewSerializer(data=request.data,context={'client': request.user, 'review_id': review_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Review updated successfully.'}, status=status.HTTP_200_OK)
    

    elif request.method == 'DELETE':
        pass
        serializer = DeleteClientReviewSerializer(data={}, context={'client': request.user, 'review_id': review_id})
        serializer.is_valid(raise_exception=True)
        serializer.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)