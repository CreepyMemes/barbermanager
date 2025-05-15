from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.models import EmailAddress
from .models import Roles, User, BarberInvitation


class ClientRegisterSerializer(RegisterSerializer):
    """
    Register a client. Default serializer for client signup.
    """
    def custom_signup(self, request, user):
        user.role = Roles.CLIENT.value
        user.save()

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

        EmailAddress.objects.create(
            user=user,
            email=email,
            verified=True,
            primary=True,
        )

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