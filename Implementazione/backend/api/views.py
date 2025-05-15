from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import BarberInvitation
from .serializers import BarberInviteSerializer, BarberRegisterSerializer


User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAdminUser])
def invite_barber(request):
    """
    Admin-only: Invite a barber by email. Sends a link with encoded email (uid).
    """
    serializer = BarberInviteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']

    invitation, created = BarberInvitation.objects.get_or_create(email=email, used=False)
    if not created:
        return Response({"detail": "Invitation already sent to this email."}, status=400)

    uid = urlsafe_base64_encode(force_bytes(email))
    token = default_token_generator.make_token(User(email=email))
    link = f"http://localhost:8000/api/register-barber/{uid}/{token}/"

    send_mail(
        subject='Invito a registrarsi su BarberManager',
        message=f'Sei stato invitato a registrarti come barbiere su BarberManager, Clicca qui per registrarti: {link}',
        from_email='barber.manager.verify@gmail.com',
        recipient_list=[email],
    )

    return Response({"detail": "Invitation sent."})


@api_view(['POST'])
def register_barber(request, uidb64, token): 
    """
    Public: Register a barber using the emailed link (uid + token).
    """
    data = request.data.copy()
    data['uid'] = uidb64
    data['token'] = token

    serializer = BarberRegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({"detail": "Barber registered successfully."})


@api_view(['POST'])
def request_password_reset(request):
    """
    Request password reset: Sends a reset link with uid + token if email exists.
    """
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"detail": "If that email exists, a reset link has been sent."})  # Do not leak existence

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = f"http://localhost:8000/api/reset-password/{uid}/{token}/"

    send_mail(
        subject='Reset your password',
        message=f'Click here to reset your password: {reset_link}',
        from_email='barber.manager.verify@gmail.com',
        recipient_list=[email],
    )

    return Response({"detail": "If that email exists, a reset link has been sent."})


@api_view(['POST'])
def confirm_password_reset(request, uidb64, token):
    """
    Confirm password reset with uid + token.
    """
    password = request.data.get('password')
    if not password:
        return Response({"error": "Password is required"}, status=400)

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        return Response({"error": "Invalid reset link"}, status=400)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired token"}, status=400)

    try:
        validate_password(password, user)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    user.set_password(password)
    user.save()

    return Response({"detail": "Password reset successful."})
