from rest_framework import serializers
from ..models import Barber


class GetBarberListSerializer(serializers.ModelSerializer):
    """
    Returns read only info for barbers
    """
    class Meta:
        model = Barber
        fields = ['id', 'username', 'email', 'is_active'] 
        read_only_fields = fields