from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from ..serializers import (
    ClientRegisterSerializer,
    LoginSerializer,
    BarberRegisterSerializer
)


User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register_client(request):
    """
    Register a client by sending an email confirmation,
    client must verify their email to login
    """
    serializer = ClientRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = f"http://localhost:8000/api/auth/verify-email/{uid}/{token}/"

        send_mail(
            subject='Verify your email on BarberManager',
            message=f'Click here to verify your account: {link}',
            from_email='barber.manager.verify@gmail.com',
            recipient_list=[user.email],
        )

        return Response({'detail': 'Email verification has been sent.'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Login method for users with email or username and password.
    It hadles unverified users accordingly
    and uses JWT token generation.
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    password = serializer.validated_data['password']

    identifier = email or username

    try:
        user = User.objects.get(email=identifier) if email else User.objects.get(username=identifier)
        
        if not user.is_active:
            return Response({'error': 'Account inactive. Please confirm your email.'}, status=status.HTTP_403_FORBIDDEN)

    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=identifier, password=password)

    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)

    return Response({
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'role': user.role,
        },
        'token': {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            "expires_in": 1800,
            "refresh_expires_in": 86400,
            "token_type": "Bearer",
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, uidb64, token):
    """
    Confirms a user's email using uid and token.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        return Response({"error": "Invalid confirmation link."}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

    user.is_active = True
    user.save()

    return Response({"detail": "Email confirmed successfully."})


@api_view(['POST'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def request_password_reset(request):
    """
    Request password reset: Sends a reset link with uid + token if email exists.
    """
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"detail": "If that email exists, a reset link has been sent."})  # Do not leak existence

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = f"http://localhost:8000/api/auth/reset-password/{uid}/{token}/"

    send_mail(
        subject='Reset your password',
        message=f'Click here to reset your password: {reset_link}',
        from_email='barber.manager.verify@gmail.com',
        recipient_list=[email],
    )

    return Response({"detail": "If that email exists, a reset link has been sent."})


@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_password_reset(request, uidb64, token):
    """
    Confirm password reset with uid + token.
    """
    password = request.data.get('password')
    if not password:
        return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_password(password, user)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(password)
    user.save()

    return Response({"detail": "Password reset successful."})
