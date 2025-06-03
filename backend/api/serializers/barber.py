from rest_framework import serializers
from ..utils import (
    BarberValidationMixin,
)
from ..models import Service


class AddServiceSerializer(BarberValidationMixin, serializers.Serializer):
    """
    Admin only: Invites a barber, accepts only email.
    """
    name = serializers.CharField(required=True, max_length=100)
    price = serializers.DecimalField(required=True, max_digits=6, decimal_places=2) 

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)

        barber = attrs['barber']
        name = attrs['name']

        if Service.objects.filter(barber=barber, name__iexact=name).exists():
            raise serializers.ValidationError(f'You already offer a service with the name: {name}.')
        
        return attrs

    def create(self, validated_data):
        barber = validated_data['barber']
        name = validated_data['name']
        price = validated_data['price']

        return Service.objects.create(
            barber=barber,
            name=name,
            price=price
        )

