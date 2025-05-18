from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers

from ..models import Client, Barber


User = get_user_model()


class ClientRegisterSerializer(serializers.ModelSerializer):
    """
    Register a client. Sends a confirmation email.
    Client must provide valid username and password
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = Client
        fields = ['email', 'username', 'password']

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username is already taken.")
        
        return username
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        return email


    def validate_password(self, value):
        validate_password(value)
        return value


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


class BarberRegisterSerializer(serializers.Serializer):
    """
    Barber completes registration via invite link. Only sets username and password.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Barber
        fields = ['username', 'password']


    def validate_password(self, value):
        validate_password(value)
        return value


    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username is already taken.")
        return username


    def create(self, validated_data):
        password = validated_data.get('password')
        username = validated_data.get('username')

        barber = self.context['barber']
        barber.username = username
        barber.set_password(password)
        barber.is_active = True
        barber.save()

        return barber
    

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
    

class PasswordResetRequestSerializer(serializers.Serializer):
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
        

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)

    def validate_password(self, value):
        user = self.context.get('user')

        if user:
            validate_password(value, user)

        return value


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