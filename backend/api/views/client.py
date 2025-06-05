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
    ReviewSerializer
)
from ..models import (
    Appointment, 
    Review, 
    AppointmentStatus
)


@api_view(['GET'])
@permission_classes([IsClientRole])
def get_client_appointments(request):
    """
    Get all appointments for the authenticated client.
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


# TODO:
@api_view(['GET'])
@permission_classes([IsClientRole])
def get_client_reviews(request):
    """
    GET: List own reviews
    """
    user = request.user
    reviews = Review.objects.filter(client=user).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsClientRole])
def create_client_review(request, appointment_id):
    """
    POST: Create a review for a completed appointment if not already reviewed
    URL: /client/reviews/<appointment_id>/
    """
    user = request.user
    try:
        appointment = Appointment.objects.get(
            id=appointment_id, 
            client=user
        )
    except Appointment.DoesNotExist:
        return Response({'detail': 'Appointment not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Inseriamo appointment nel payload per la validazione
    data = request.data.copy()
    data['appointment'] = appointment.id

    serializer = ReviewSerializer(data=data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save(client=user)  # barber verrà settato dal create() del serializer
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsClientRole])
def edit_client_review(request, review_id):
    """
    PATCH: Edit own review
    URL: /client/reviews/<review_id>/
    """
    user = request.user
    try:
        review = Review.objects.get(id=review_id, client=user)
    except Review.DoesNotExist:
        return Response({'detail': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(review, data=request.data, partial=True, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsClientRole])
def delete_client_review(request, review_id):
    """
    DELETE: Delete own review
    URL: /client/reviews/<review_id>/
    """
    user = request.user
    try:
        review = Review.objects.get(id=review_id, client=user)
    except Review.DoesNotExist:
        return Response({'detail': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)

    review.delete()
    return Response({'detail': 'Review deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
