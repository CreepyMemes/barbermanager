from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers
from ..models import User, Client
from ..utils import (
    UserValidationMixin,
    UsernameValidationMixin,
    EmailValidationMixin, 
    PasswordValidationMixin,
    PhoneNumberValidationMixin,
    UIDTokenValidationSerializer,
)

class GetCurrentUserSerializer(UserValidationMixin, serializers.Serializer):
    """
    Returns common information related to the profile of a given user
    """
    def validate(self, attrs):
        attrs = self.validate_user(attrs)
        return attrs

    def to_representation(self, validated_data):
        user = validated_data['user']
        return {'me': user.to_dict()}
    

class RegisterClientSerializer(UsernameValidationMixin, EmailValidationMixin, PasswordValidationMixin, PhoneNumberValidationMixin, serializers.Serializer):
    """
    Register a client. Sends a confirmation email.
    Client must provide valid username and password
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    surname = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=False)

    def validate(self, attrs):
        attrs = self.validate_username_format(attrs)
        attrs = self.validate_username_unique(attrs)
        attrs = self.validate_email_unique(attrs)
        attrs = self.validate_phone_number_format(attrs)
        
        return attrs
    
    def create(self, validated_data):
        client = Client(
            email=validated_data['email'], 
            username=validated_data['username'], 
            name=validated_data['name'],
            surname=validated_data['surname'],
            is_active=False
        )

        if 'phone_number' in validated_data:
            client.phone_number = validated_data['phone_number']

        client.set_password(validated_data['password'])
        client.save()

        return client


class RegisterBarberSerializer(UIDTokenValidationSerializer, UsernameValidationMixin, PasswordValidationMixin, serializers.Serializer):
    """
    Barber completes registration via invite link. Only sets username and password.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    name = serializers.CharField(required=True)
    surname = serializers.CharField(required=True)
    description = serializers.CharField(required=False)

    def validate(self, attrs):
        attrs = self.validate_uid_token(attrs)
        attrs = self.validate_username_unique(attrs)

        if attrs['user'].is_active:
            raise serializers.ValidationError('Account already registered.')

        return attrs
    
    def create(self, validated_data):
        barber = validated_data['user']
        barber.username = validated_data['username']
        barber.name = validated_data['name']
        barber.surname = validated_data['surname']
        barber.is_active = True

        if 'description' in validated_data:
            barber.description = validated_data['description']

        barber.set_password(validated_data['password'])
        barber.save()

        return barber


class GetEmailFromTokenSerializer(UIDTokenValidationSerializer, serializers.Serializer):
    """
    Returns the email associated to the user from a valid given uid64 and token
    """
    def validate(self, attrs):
        attrs = self.validate_uid_token(attrs)
        return attrs
    
    def to_representation(self, validated_data):
        user = validated_data['user']
        return {'email': user.email}


class VerifyClientEmailSerializer(UIDTokenValidationSerializer):
    """
    Handles token validations when a client attempts to verify their account
    """
    def validate(self, attrs):
        attrs = self.validate_uid_token(attrs)

        if attrs['user'].is_active:
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
            'user': user.to_dict(),
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

    def validate(self, attrs):
        attrs = self.validate_uid_token(attrs)
        return attrs
    
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
