from rest_framework import serializers
from ..models import (
    Barber,
)


class GetBarberListSerializer(serializers.Serializer):
    """
    Return a list of all active barbers
    """
    def get_barbers(self):
        barbers = Barber.objects.filter(is_active=True)
        return [{"id": b.id, "username": b.username, "description": b.description} for b in barbers]

    def to_representation(self, instance):
        barbers = self.get_barbers()
        return {'barbers': barbers}