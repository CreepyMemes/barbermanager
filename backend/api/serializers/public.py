from rest_framework import serializers
from ..utils import (
    BarberValidationMixin,
)
from ..models import (
    Barber,
    Availability,
    Service,
)


class GetBarberListSerializer(serializers.Serializer):
    """
    Return a list of all active barbers
    """

    def to_representation(self, instance):
        barbers = Barber.objects.filter(is_active=True)

        return {"barbers": [{
            "id": b.id, 
            "username": b.username, 
            "description": b.description
        } for b in barbers]}


class GetBarberAvailabilitySerializer(BarberValidationMixin, serializers.Serializer):
    """
    Returns all availabilities for a barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs
    
    def get_availabilities(self, barber_id):
        availabilities = Availability.objects.filter(barber_id=barber_id)
        return [{'date': a.date, 'slots': a.slots} for a in availabilities]

    def to_representation(self, validated_data):
        barber = validated_data['barber']
        availabilities = self.get_availabilities(barber.id)
        return {'availability': availabilities}
    

class GetBarberServicesSerializer(BarberValidationMixin, serializers.Serializer):
    """
    Returns all availabilities for a barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs
    
    def get_services(self, barber_id):
        services = Service.objects.filter(barber_id=barber_id)
        return [{'name': s.name, 'price': s.price} for s in services]

    def to_representation(self, validated_data):
        barber = validated_data['barber']
        services = self.get_services(barber.id)
        return {'services': services}