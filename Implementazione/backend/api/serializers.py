from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import Roles, User

class ClientRegisterSerializer(RegisterSerializer):
    def custom_signup(self, request, user):
        user.role = Roles.CLIENT.value
        user.save()

class BarberInviteSerializer(serializers.Serializer):
    email = serializers.EmailField()
