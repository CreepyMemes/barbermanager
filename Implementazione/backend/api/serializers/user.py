from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from ..models import BarberInvitation, Roles
from ..utils import generate_unique_username


User = get_user_model()


class ClientRegisterSerializer(serializers.ModelSerializer):
    """
    Register a client. Sends a confirmation email.
    Sets fallback username based on email if not present
    """
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def validate_password(self, value):
        validate_password(value)
        return value


    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data.get('username') or generate_unique_username(email)
    
        user = User.objects.create(
            email=email,
            username=username,
            role=Roles.CLIENT.value,
            is_active=False,
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    """
    Login using either email or username, not both.
    """
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if not email and not username:
            raise serializers.ValidationError({"error": "You must provide either an email or username."})
        if email and username:
            raise serializers.ValidationError({"error": "Provide only one of email or username, not both."})

        data['identifier'] = email or username
        
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Get information on currently logged in user
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class BarberInviteSerializer(serializers.Serializer):
    """
    Invite a barber: accept only email.
    """
    email = serializers.EmailField()


class BarberRegisterSerializer(serializers.Serializer):
    """
    Register a barber: requires uid and token, validates passwords.
    """
    uid = serializers.CharField()
    token = serializers.UUIDField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        validate_password(data['password'])
        return data


    def save(self):
        try:
            email = urlsafe_base64_decode(self.validated_data['uid']).decode()
        except (ValueError, TypeError, UnicodeDecodeError):
            raise serializers.ValidationError({"error": "Invalid UID."})

        token = self.validated_data['token']

        try:
            invitation = BarberInvitation.objects.get(email=email, used=False)
        except BarberInvitation.DoesNotExist:
            raise serializers.ValidationError({"error": "Invalid or expired invitation."})

        if invitation.token != token:
            raise serializers.ValidationError({"error": "Invalid invitation token."})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "User with this email already exists."})

        user = User.objects.create(
            email=email,
            username=generate_unique_username(email),
            role=Roles.BARBER.value,
            is_active=True,
        )
        user.set_password(self.validated_data['password'])
        user.save()

        invitation.used = True
        invitation.save()

        return user