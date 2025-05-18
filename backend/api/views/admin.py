from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from ..utils import (
    IsAdminRole,
    send_barber_invite_email,
)
from ..serializers import (
    InviteBarberSerializer,
    DeleteBarberSerializer,
)


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