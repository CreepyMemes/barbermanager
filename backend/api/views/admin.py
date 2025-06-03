from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..utils import (
    IsAdminRole,
    send_barber_invite_email,
)
from ..serializers import (
    InviteBarberSerializer,
    DeleteBarberSerializer,
    AvailabilitySerializer,
)
from ..models import Availability


@api_view(['POST'])
@permission_classes([IsAdminRole])
def invite_barber(request):
    """
    Admin-only: Invite a barber by email. Sends a link with encoded email (uid).
    """
    serializer = InviteBarberSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    barber = serializer.save()

    uid = urlsafe_base64_encode(force_bytes(barber.pk))
    token = default_token_generator.make_token(barber)
    send_barber_invite_email(barber.email, uid, token, settings.FRONTEND_URL)

    return Response({'detail': 'Barber invited successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAdminRole])
def delete_barber(request, barber_id):
    """
    Deletes a barber by ID using the serializer
    """
    serializer = DeleteBarberSerializer(data={"id": barber_id})
    serializer.is_valid(raise_exception=True)
    serializer.delete()

    return Response({"detail": f"Barber with ID {barber_id} has been deleted."}, status=status.HTTP_200_OK)


@api_view(['POST', 'PATCH', 'DELETE'])
@permission_classes([IsAdminRole])
def manage_barber_availability(request, barber_id):
    date = request.data.get('date')
    if not date:
        return Response({"detail": "Date is required."}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        slots = request.data.get('slots')
        if not slots:
            return Response({"detail": "Slots are required for POST."}, status=status.HTTP_400_BAD_REQUEST)
        availability, created = Availability.objects.update_or_create(
            barber_id=barber_id,
            date=date,
            defaults={'slots': slots}
        )
        serializer = AvailabilitySerializer(availability)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    elif request.method == 'PATCH':
        try:
            availability = Availability.objects.get(barber_id=barber_id, date=date)
        except Availability.DoesNotExist:
            return Response({"detail": "Availability not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AvailabilitySerializer(availability, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            availability = Availability.objects.get(barber_id=barber_id, date=date)
            availability.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Availability.DoesNotExist:
            return Response({"detail": "Availability not found."}, status=status.HTTP_404_NOT_FOUND)