from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from ..models import BarberInvitation, Roles


User = get_user_model()


class ClientRegisterSerializer(serializers.ModelSerializer):
    """
    Register a client. Sends a confirmation email.
    Sets fallback username based on email if not present
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_password(self, value):
        validate_password(value)
        return value


    def create(self, validated_data):
        email = validated_data['email']
        username = self.generate_unique_username(email)
    
        user = User.objects.create(
            email=email,
            username=username,
            role=Roles.CLIENT.value,
            is_active=False,
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


    def generate_unique_username(self, email):
        base = email.split('@')[0]
        username = base
        count = 1

        while User.objects.filter(username=username).exists():
            username = f"{base}_{count}"
            count += 1

        return username


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
            raise serializers.ValidationError("You must provide either an email or username.")
        if email and username:
            raise serializers.ValidationError("Provide only one of email or username, not both.")

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
    token = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)


    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        
        validate_password(data['password1'])

        return data


    def save(self):
        email = urlsafe_base64_decode(self.validated_data['uid']).decode()
        token = self.validated_data['token']

        try:
            invitation = BarberInvitation.objects.get(email=email, used=False)
        except BarberInvitation.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired invitation.")

        temp_user = User(email=email)
        from django.contrib.auth.tokens import default_token_generator
        if not default_token_generator.check_token(temp_user, token):
            raise serializers.ValidationError("Invalid token.")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists")
        
        user = User.objects.create(
            email=email,
            username=self.generate_unique_username(email),
            role=Roles.BARBER.value,
            is_active=True,
        )
        user.set_password(self.validated_data['password1'])
        user.save()

        invitation.used = True
        invitation.save()

        return user
    

    def generate_unique_username(self, email):
        base = email.split('@')[0]
        username = base
        count = 1

        while User.objects.filter(username=username).exists():
            username = f"{base}_{count}"
            count += 1

        return username