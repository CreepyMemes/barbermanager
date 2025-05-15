from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import Roles, User
from .serializers import BarberInviteSerializer

@api_view(['POST'])
@permission_classes([IsAdminUser])
def invite_barber(request):
    serializer = BarberInviteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']

    uid = urlsafe_base64_encode(force_bytes(email))
    domain = get_current_site(request).domain
    link = f"http://{domain}/register-barber/{uid}/"

    send_mail(
        'Invito a registrarsi su BarberManager',
        f'Sei stato invitato a registrarti come barbiere su BarberManager, Clicca qui per registrarti: {link}',
        'barber.manager.verify@gmail.com',
        [email],
    )
    return Response({"detail": "Invitation sent."})
