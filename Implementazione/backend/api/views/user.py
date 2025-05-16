from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from ..permissions import IsAdminRole
from ..models import BarberInvitation
from ..serializers import (
    GetUserSerializer,
    BarberInviteSerializer,
)


User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAdminRole])
def invite_barber(request):
    """
    Admin-only: Invite a barber by email. Sends a link with encoded email (uid).
    """
    serializer = BarberInviteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']

    if User.objects.filter(email=email).exists():
        return Response({"detail": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

    invitation, created = BarberInvitation.objects.get_or_create(email=email, used=False)
    if not created:
        return Response({"detail": "Invitation already sent to this email."}, status=status.HTTP_400_BAD_REQUEST)

    uid = urlsafe_base64_encode(force_bytes(email))
    token = str(invitation.token)
    link = f"{settings.FRONTEND_URL}/api/auth/register-barber/{uid}/{token}/"

    send_mail(
        subject='Invito a registrarti su BarberManager',
        message=f'Sei stato invitato a registrarti come barbiere su BarberManager, Clicca qui per registrarti: {link}',
        from_email='barber.manager.verify@gmail.com',
        recipient_list=[email],
    )

    return Response({"detail": "Invitation sent."})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    """
    Return the authenticated user's information.
    """
    serializer = GetUserSerializer(request.user)
    return Response(serializer.data)