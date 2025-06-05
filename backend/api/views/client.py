from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.utils.permissions import IsClientRole
from api.models.appointment import Appointment, Review, AppointmentStatus
from api.serializers.client import (
    AppointmentSerializer,
    AppointmentCreateSerializer,
    ReviewSerializer
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsClientRole])
def client_appointments_list_create(request):
    """
    GET:  List own past appointments (COMPLETED or CANCELLED)
    POST: Create a new appointment only if no ONGOING currently
    """
    user = request.user
    client = user.client  

    if request.method == 'GET':
        past_appointments = Appointment.objects.filter(
            client=client,
            status__in=[AppointmentStatus.COMPLETED.value, AppointmentStatus.CANCELLED.value]
        ).order_by('-date', '-slot')
        serializer = AppointmentSerializer(past_appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if Appointment.objects.filter(client=client, status=AppointmentStatus.ONGOING.value).exists():
        return Response({'detail': 'You already have an ongoing appointment.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = AppointmentCreateSerializer(data=request.data, context={'client': client})
    serializer.is_valid(raise_exception=True)
    appointment = serializer.save()  
    response_serializer = AppointmentSerializer(appointment)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsClientRole])
def client_appointment_delete(request, appointment_id):
    """
    DELETE: Cancel an ongoing appointment if it belongs to the client
    """
    user = request.user
    try:
        appointment = Appointment.objects.get(id=appointment_id, client=user)
    except Appointment.DoesNotExist:
        return Response({'detail': 'Appointment not found.'}, status=status.HTTP_404_NOT_FOUND)

    if appointment.status != AppointmentStatus.ONGOING.value:
        return Response({'detail': 'Cannot cancel a non-ongoing appointment.'}, status=status.HTTP_400_BAD_REQUEST)

    appointment.status = AppointmentStatus.CANCELLED.value
    appointment.save()
    return Response({'detail': 'Appointment cancelled successfully.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsClientRole])
def client_reviews_list(request):
    """
    GET: List own reviews
    """
    user = request.user
    reviews = Review.objects.filter(client=user).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsClientRole])
def client_review_create(request, appointment_id):
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
@permission_classes([IsAuthenticated, IsClientRole])
def client_review_edit(request, review_id):
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
@permission_classes([IsAuthenticated, IsClientRole])
def client_review_delete(request, review_id):
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
