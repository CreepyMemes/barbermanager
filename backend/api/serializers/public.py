from rest_framework import serializers
from ..utils import (
    BarberValidationMixin,
)
from ..models import (
    Barber,
    Availability,
    Service,
    Review,
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
    

class GetBarberProfileSerializer(BarberValidationMixin, serializers.Serializer):
    """
    Returns all the public information of the profile of a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs

    def get_services(self, barber_id):
        services = Service.objects.filter(barber_id=barber_id)
        return [{
            'name': s.name, 
            'price': s.price
        } for s in services]
    
    def get_reviews(self, barber_id):
        reviews = Review.objects.filter(barber_id=barber_id).select_related('client', 'appointment')
        return [{
            'client': r.client.username,
            'rating': r.rating,
            'comment': r.comment,
            'created_at': r.created_at.strftime('%Y-%m-%d'),
            'edited_at': r.edited_at.strftime('%Y-%m-%d') if r.edited_at else None
        } for r in reviews]
    
    def to_representation(self, validated_data):
        barber = validated_data['barber']
        services = self.get_services(barber.id)
        reviews = self.get_reviews(barber)
        return {
            'profile': {
                'services': services,
                'reviews': reviews,
        }
    }