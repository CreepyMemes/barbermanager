from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


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