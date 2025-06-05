from rest_framework import serializers
from ..utils import (
    BarberValidationMixin,
    NewServiceValidationMixin,
    FindServiceValidationMixin,
)
from ..models import (
    Service,
    Appointment,
)


class CreateServiceSerializer(BarberValidationMixin, NewServiceValidationMixin, serializers.Serializer):
    """
    Barber only: Creates a new service (name/price) for the barber.
    """
    name = serializers.CharField(required=True, max_length=100)
    price = serializers.DecimalField(required=True, max_digits=6, decimal_places=2) 

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_new_service(attrs)
        return attrs

    def create(self, validated_data):
        return Service.objects.create(**validated_data)
    

class UpdateServiceSerializer(BarberValidationMixin, FindServiceValidationMixin, serializers.Serializer):
    """
    Barber only: Updates an existing service, for a given barber.
    """
    name = serializers.CharField(required=True, max_length=100)
    price = serializers.DecimalField(required=True, max_digits=6, decimal_places=2)

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_find_service(attrs)
        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.price = validated_data['price']
        instance.save()
        return instance

    def save(self, **kwargs):
        return self.update(self.validated_data['service'], self.validated_data)


class DeleteServiceSerializer(BarberValidationMixin, FindServiceValidationMixin, serializers.Serializer):
    """
    Barber only: Deletes a service for a given barber.
    """
    name = serializers.CharField(required=True, max_length=100)

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_find_service(attrs)
        return attrs

    def delete(self):
        self.validated_data['service'].delete()


class AppointmentSerializer(serializers.ModelSerializer):
    client_email = serializers.CharField(source='client.email', read_only=True)
    services = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Appointment
        fields = ['id', 'client_email', 'date', 'slot', 'services', 'status']