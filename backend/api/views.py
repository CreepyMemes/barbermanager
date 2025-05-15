from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .serializers import BarberInviteSerializer
from .models import BarberInvitation


# Defines the api endpoint to invite a barber to register by email, only admin can access
@api_view(['POST'])
@permission_classes([IsAdminUser])
def invite_barber(request):
    serializer = BarberInviteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']

    # Save invitation (or get existing)
    invitation, created = BarberInvitation.objects.get_or_create(email=email, used=False)
    if not created:
        return Response({"detail": "Invitation already sent to this email."}, status=400)

    uid = urlsafe_base64_encode(force_bytes(email))
    link = f"http://localhost:8000/register-barber/{uid}/"

    send_mail(
        'Invito a registrarsi su BarberManager',
        f'Sei stato invitato a registrarti come barbiere su BarberManager, Clicca qui per registrarti: {link}',
        'barber.manager.verify@gmail.com',
        [email],
    )
    return Response({"detail": "Invitation sent."})

# Defines the api endpoint to register as an invited barber
@api_view(['POST'])
def register_barber(request):
    from .serializers import BarberRegisterSerializer

    serializer = BarberRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"detail": "Barber registered successfully."})
