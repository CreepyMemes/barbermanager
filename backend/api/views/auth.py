from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from ..utils import(
    send_client_verify_email,
    send_password_reset_email,
)
from ..serializers import (
    ClientRegisterSerializer,
    LoginSerializer,
    BarberRegisterSerializer,
    LogoutSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    RefreshTokenCustomSerializer,
    GetUserSerializer,
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
    serializer.is_valid(raise_exception=True)
    client = serializer.save()

    uid = urlsafe_base64_encode(force_bytes(client.pk))
    token = default_token_generator.make_token(client)
    send_client_verify_email(client.email, uid, token, settings.FRONTEND_URL)

    return Response({'detail': 'Client registered, check your email to verify.'}, status=status.HTTP_201_CREATED)


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
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({'detail': 'Barber registered and account activated.'})
    

@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def verify_client(request, uidb64, token):
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
@permission_classes([AllowAny])
@authentication_classes([]) 
def login_user(request):
    """
    Login with email OR username + password.
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout by blacklisting the refresh token.
    """
    serializer = LogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return Response({'detail': 'Logout successful.'}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def request_password_reset(request):
    """
    Request password reset by email, sends reset email with token.
    """
    serializer = PasswordResetRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.get_user()
  
    if user: # Fail silently for security
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

    serializer = PasswordResetConfirmSerializer(data=request.data, context={'user': user})
    serializer.is_valid(raise_exception=True)
    user.set_password(serializer.validated_data['password'])
    user.save()

    return Response({'detail': 'Password has been reset successfully.'})


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def refresh_token(request):
    """
    Refresh the access token using a refresh token passed as 'refresh_token' in the request.
    """
    serializer = RefreshTokenCustomSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.get_response(), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    """
    Return the authenticated user's information.
    """
    serializer = GetUserSerializer(request.user)
    return Response(serializer.data)