from rest_framework import serializers
from ..utils import (
    BarberValidationMixin,
    ServiceValidationMixin
)
from ..models import Service


class AddServiceSerializer(BarberValidationMixin, serializers.Serializer):
    """
    Barber only: Invites a barber, accepts only email.
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


class UpdateServiceSerializer(ServiceValidationMixin, serializers.Serializer):
    """
    Barber only: Invites a service, accepts only email.
    """
    name = serializers.CharField(required=True, max_length=100)
    price = serializers.DecimalField(required=True, max_digits=6, decimal_places=2) 

    def validate(self, attrs):
        attrs = self.validate_service(attrs)
        return attrs

    def update(self, instance, validated_data):
        name = validated_data['name']
        price = validated_data['price']
        instance.name = name
        instance.price = price
        instance.save()
        return instance
    
    def save(self, **kwargs):
        return self.update(self.validated_data['service'], self.validated_data)
    


class DeleteServiceSerializer(serializers.Serializer):
    """
    Barber only: Deletes a service by ID if they exist
    """
    id = serializers.IntegerField(required=True)

    def validate_id(self, value):

        try:
            self.service = Service.objects.get(id=value)
        except Service.DoesNotExist:
            raise serializers.ValidationError("Service with this ID does not exist.")  
        
        return value
    
    def delete(self):
        self.service.delete()
        return self.service
    