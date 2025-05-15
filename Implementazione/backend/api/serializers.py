from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.models import EmailAddress
from rest_framework import serializers
from .models import Roles, User, BarberInvitation


# Serializer for registering as a client
class ClientRegisterSerializer(RegisterSerializer):
    def custom_signup(self, request, user):
        user.role = Roles.CLIENT.value
        user.save()


# Serializer for inviting a barber to register
class BarberInviteSerializer(serializers.Serializer):
    email = serializers.EmailField()


# Serializer for registering as an invited barber
class BarberRegisterSerializer(serializers.Serializer):
    uid = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        validate_password(data['password1'])
        return data

    def save(self):
        try:
            email = urlsafe_base64_decode(self.validated_data['uid']).decode()
        except Exception:
            raise serializers.ValidationError("Invalid or corrupted registration link")

        # Check invitation exists and unused
        try:
            invitation = BarberInvitation.objects.get(email=email, used=False)
        except BarberInvitation.DoesNotExist:
            raise serializers.ValidationError("No valid invitation found for this email")

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

        # Mark email as verified for allauth
        EmailAddress.objects.create(
            user=user,
            email=email,
            verified=True,
            primary=True,
        )
        return user
    
    # Generate a unique username based on email
    def generate_unique_username(self, email):
        base = email.split('@')[0]
        username = base
        count = 1
        from .models import User
        while User.objects.filter(username=username).exists():
            username = f"{base}_{count}"
            count += 1
        return username