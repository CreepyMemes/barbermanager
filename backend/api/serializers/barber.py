from rest_framework import serializers
from ..utils import (
    BarberValidationMixin,
)
from ..models import Service



class AddServiceSerializer(BarberValidationMixin, serializers.Serializer):
    """
    Admin only: Invites a barber, accepts only email.
    """
    name = serializers.CharField(required=True) # TODO: add unique validation
    price = serializers.DecimalField(required=True) 

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs

    def create(self, validated_data):
        barber = validated_data['barber']
        name = validated_data['name']
        price = validated_data['price']

        return Service.objects.create(
            barber,
            name,
            price
        )

