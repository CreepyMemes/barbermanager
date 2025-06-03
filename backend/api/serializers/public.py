from rest_framework import serializers
from ..models import (
    Barber,
    Availability,
)


class GetBarberListSerializer(serializers.ModelSerializer):
    """
    Returns read only info for barbers
    """
    class Meta:
        model = Barber
        fields = ['id', 'username', 'email'] 
        read_only_fields = fields


class GetBarberAvailabilitySerializer(serializers.Serializer):
    """
    Returns all availabilities for a barber
    """
    barber_id = serializers.IntegerField(required=True)
    availabilities = serializers.SerializerMethodField(read_only=True)

    def validate(self, data):
        barber_id = data['barber_id']

        if not Barber.objects.filter(id=barber_id, is_active=True).exists():
            raise serializers.ValidationError('Barber does not exist.')
        
        return data
    
    def get_availabilities(self, barber_id):
        availabilities = Availability.objects.filter(barber_id=barber_id)
        return [{'date': a.date, 'slots': a.slots} for a in availabilities]

    def to_representation(self, instance):
        barber_id = instance['barber_id']
        availabilities = self.get_availabilities(barber_id)
        return {'availability': availabilities}