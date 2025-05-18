from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers
from ..models import User, Client
from ..utils import (
    get_user_from_uid_token, 
    UsernameValidationMixin,
    EmailValidationMixin, 
    PasswordValidationMixin,
    UIDTokenValidationSerializer,
)


class RegisterClientSerializer(UsernameValidationMixin, EmailValidationMixin, PasswordValidationMixin, serializers.Serializer):
    """
    Register a client. Sends a confirmation email.
    Client must provide valid username and password
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True)

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        password = validated_data.get('password')
    
        client = Client(
            email=email,
            username=username,
            is_active=False,
        )
        client.set_password(password)
        client.save()

        return client


class RegisterBarberSerializer(UsernameValidationMixin, PasswordValidationMixin, serializers.Serializer):
    """
    Barber completes registration via invite link. Only sets username and password.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        uidb64 = self.context.get('uidb64')
        token = self.context.get('token')

        if not uidb64 or not token:
            raise serializers.ValidationError("Missing uid or token.")
        
        barber = get_user_from_uid_token(uidb64, token)
        attrs['barber'] = barber

        if barber.is_active:
            raise serializers.ValidationError('Account already registered.')

        return attrs
    
    def create(self, validated_data):
        barber = self.validated_data['barber']
        password = validated_data.get('password')
        username = validated_data.get('username')

        barber.username = username
        barber.set_password(password)
        barber.is_active = True
        barber.save()

        return barber


class VerifyClientEmailSerializer(UIDTokenValidationSerializer):
    """
    Handles token validations when a client attempts to verify their account
    """
    def validate(self, attrs):
        attrs = super().validate(attrs)
        client = attrs.get('user')

        if client.is_active:
            raise serializers.ValidationError('Account already verified.')

        return attrs

    def save(self, **kwargs):
        client = self.validated_data['user']

        client.is_active = True
        client.save()

        return client
    

class LoginSerializer(serializers.Serializer):
    """
    Login using either email or username, not both.
    """
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not email and not username:
            raise serializers.ValidationError("You must provide either an email or username.")
        if email and username:
            raise serializers.ValidationError("Provide only one of email or username, not both.")

        identifier = username or email

        user = authenticate(username=identifier, password=password)

        if not user:
            raise PermissionDenied('Invalid credentials.')

        if not user.is_active:
            raise PermissionDenied('Account inactive. Please verify your email.')

        data['user'] = user
        data['refresh'] = RefreshToken.for_user(user)

        return data

    def to_representation(self, instance):
        user = instance['user']
        refresh = instance['refresh']

        return {
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': getattr(user, 'role', None),
            },
            'token': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'expires_in': int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds()),
                'refresh_expires_in': int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()),
                'token_type': 'Bearer',
            }
        }


class LogoutSerializer(serializers.Serializer):
    """
    Logout by blacklisting entered refresh token
    """
    refresh_token = serializers.CharField(required=True)

    def validate_refresh_token(self, value):
        try:
            self.token = RefreshToken(value)
        except TokenError:
            raise serializers.ValidationError("Invalid or expired refresh token.")
        
        return value
    
    def save(self, **kwargs):
        try:
            self.token.blacklist()
        except AttributeError:
            raise serializers.ValidationError("Token blacklisting not supported.")
    

class RequestPasswordResetSerializer(serializers.Serializer):
    """
    Request password reset by email associated to account
    """
    email = serializers.EmailField(required=True)

    def get_user(self):
        email = self.validated_data.get('email')

        try:
            user = User.objects.get(email=email, is_active=True)
            return user
        except User.DoesNotExist:
            return  # Silently continue for security
        

class ConfirmPasswordResetSerializer(PasswordValidationMixin, UIDTokenValidationSerializer):
    """
    Resets a user's password after validating the request token and password
    """
    password = serializers.CharField(required=True, write_only=True)

    def save(self, **kwargs):
        user = self.validated_data['user']
        password = self.validated_data['password']

        user.set_password(password)
        user.save()

        return user


class RefreshTokenCustomSerializer(TokenRefreshSerializer):
    """
    Custom refresh token serializer for field name 'refresh_token'
    """
    refresh = None
    refresh_token = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        attrs['refresh'] = attrs.pop('refresh_token')

        try:
            validated_data = super().validate(attrs)
        except TokenError as e:
            raise serializers.ValidationError({'refresh_token': [str(e)]})
        
        return validated_data
    
    def get_response(self):
        return {
            'access_token': self.validated_data['access'],
            'expires_in': int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds()),
            'token_type': 'Bearer',
        }
    

class GetUserSerializer(serializers.ModelSerializer):
    """
    Get information on currently logged in user
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        read_only_fields = fields 