from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from ..permissions import IsAdminRole
from ..utils import(
    send_client_verify_email,
    send_barber_invite_email,
    send_password_reset_email,
)
from ..serializers import (
    ClientRegisterSerializer,
    LoginSerializer,
    BarberInviteSerializer,
    BarberRegisterSerializer,
)


User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def register_client(request):
    """
    Client self registration. Creates inactive client and sends confirmation email.
    """
    serializer = ClientRegisterSerializer(data=request.data)

    if serializer.is_valid():
        client = serializer.save()

        uid = urlsafe_base64_encode(force_bytes(client.pk))
        token = default_token_generator.make_token(client)

        send_client_verify_email(client.email, uid, token, settings.FRONTEND_URL)

        return Response({'detail': 'Client registered, check your email to verify.'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def verify_client_email(request, uidb64, token):
    """
    Verifies client account from confirmation email link.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        client = User.objects.get(pk=uid, role='CLIENT')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'detail': 'Invalid verification link.'}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(client, token):
        return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

    if client.is_active:
        return Response({'detail': 'Account already verified.'}, status=status.HTTP_400_BAD_REQUEST)
    
    client.is_active = True
    client.save()

    return Response({'detail': 'Email verified successfully.'})


@api_view(['POST'])
@permission_classes([IsAdminRole])
def invite_barber_email(request):
    """
    Admin-only: Invite a barber by email. Sends a link with encoded email (uid).
    """
    serializer = BarberInviteSerializer(data=request.data)

    if serializer.is_valid():
        barber = serializer.save()

        uid = urlsafe_base64_encode(force_bytes(barber.pk))
        token = default_token_generator.make_token(barber)

        send_barber_invite_email(barber.email, uid, token, settings.FRONTEND_URL)

        return Response({'detail': 'Barber invited successfully.'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def register_barber(request, uidb64, token): 
    """
    Barber completes registration via invite link by setting username and password.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        barber = User.objects.get(pk=uid, role='BARBER')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'detail': 'Invalid invitation link.'}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(barber, token):
        return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if barber.is_active:
        return Response({'detail': 'Account already registered.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    serializer = BarberRegisterSerializer(data=request.data, context={'barber': barber})

    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Barber registered and account activated.'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def login_user(request):
    """
    Login with email OR username + password.
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    password = serializer.validated_data['password']

    identifier = username or email

    user = authenticate(request, username=identifier, password=password)

    if not user:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.is_active:
        return Response({'detail': 'Account inactive. Please verify your email.'}, status=status.HTTP_403_FORBIDDEN)

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
            'expires_in': int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds()),
            'refresh_expires_in': int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()),
            'token_type': 'Bearer',
        }

    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout by blacklisting the refresh token.
    """
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({'refresh_token': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception as e:
        return Response({'detail': 'Invalid token or token already blacklisted.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'Logout successful.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def request_password_reset(request):
    """
    Request password reset by email, sends reset email with token.
    """
    email = request.data.get('email')
    if not email:
        return Response({'email': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email, is_active=True)
    except User.DoesNotExist:
        return Response({'detail': 'If this email is registered, a password reset email has been sent.'})

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    send_password_reset_email(user.email, uid, token, settings.FRONTEND_URL)

    return Response({'detail': 'If this email is registered, a password reset email has been sent.'})


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def confirm_password_reset(request, uidb64, token):
    """
    Confirm password reset by setting new password.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid, is_active=True)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

    new_password = request.data.get('password')
    if not new_password:
        return Response({'password': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        validate_password(new_password, user)
    except Exception as e:
        return Response({'password': list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'detail': 'Password has been reset successfully.'})


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def refresh_token(request):
    """
    Refresh the access token using a refresh token passed as 'refresh_token' in the request.
    """
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({'refresh_token': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

    serializer = TokenRefreshSerializer(data={'refresh': refresh_token})

    try:
        serializer.is_valid(raise_exception=True)
    except TokenError as e:
        return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({
        'access_token': serializer.validated_data['access'],
        'expires_in': int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds()),
        'token_type': 'Bearer',
    }, status=status.HTTP_200_OK)