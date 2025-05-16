from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class GetUserSerializer(serializers.ModelSerializer):
    """
    Get information on currently logged in user
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']