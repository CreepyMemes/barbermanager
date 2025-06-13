from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..utils import (
    IsClientRole,
)
from api.serializers.client import (
    GetClientAppointmentsSerializer,
    CreateClientAppointmentSerializer,
    CancelClientAppointmentSerializer,
    GetClientReviewsSerializer,
    CreateClientReviewSerializer,
    UpdateClientReviewSerializer,
    DeleteClientReviewSerializer,
)


@api_view(['GET'])
@permission_classes([IsClientRole])
def get_client_appointments(request):
    """
    Client only: Get all appointments for the authenticated client.
    """
    serializer = GetClientAppointmentsSerializer(data={}, context={'client_id': request.user})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsClientRole])
def create_client_appointment(request, barber_id):
    """
    Client only: Creates an appointmentt for the authenticated client.
    """
    serializer = CreateClientAppointmentSerializer(data=request.data, context={'client_id': request.user, 'barber_id': barber_id})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({'detail': 'Appointment added successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsClientRole])
def cancel_client_appointment(request, appointment_id):
    """
    Client only: Cancels an ONGOING appointment by setting it's status to CANCELLED, for the authenticated client.
    """
    serializer = CancelClientAppointmentSerializer(data={}, context={'client_id': request.user, 'appointment_id': appointment_id})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({'detail': 'Appointment cancelled successfully.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsClientRole])
def get_client_reviews(request):
    """
    Get all reviews posted by the authenticated client.
    """
    serializer = GetClientReviewsSerializer(data={}, context={'client_id': request.user})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsClientRole])
def create_client_review(request, appointment_id):
    """
    Client only:  Creates a new review post for the barber associated to the authenticated client's appointment
    """
    serializer = CreateClientReviewSerializer(data=request.data,context={'client_id': request.user, 'appointment_id': appointment_id})
    serializer.is_valid(raise_exception=True)
    serializer.create(serializer.validated_data)

    return Response({'detail': 'Review created successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsClientRole])
def manage_client_reviews(request, review_id):
    """
    Edit or delete a review by the authenticated client.
    PATCH: Update rating or comment.
    DELETE: Remove the review.
    """
    if request.method == 'PATCH':
        serializer = UpdateClientReviewSerializer(data=request.data,context={'client_id': request.user, 'review_id': review_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Review updated successfully.'}, status=status.HTTP_200_OK)
    

    elif request.method == 'DELETE':
        pass
        serializer = DeleteClientReviewSerializer(data={}, context={'client_id': request.user, 'review_id': review_id})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        return Response({'detail': 'Review deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)