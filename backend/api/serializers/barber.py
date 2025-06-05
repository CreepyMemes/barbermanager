from rest_framework import serializers
from ..utils import (
    BarberValidationMixin,
    ServiceValidationMixin,
    FindServiceValidationMixin,
)
from ..models import (
    Service,
    Appointment,
    Availability,
)


class GetBarberAvailabilitiesSerializer(BarberValidationMixin, serializers.Serializer):
    """
    Barber only: Returns all availabilities for a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs
    
    def get_availabilities(self, barber_id):
        availabilities = Availability.objects.filter(barber_id=barber_id)
        return [{'id': a.id, 'date': a.date, 'slots': a.slots} for a in availabilities]

    def to_representation(self, validated_data):
        barber = validated_data['barber']
        availabilities = self.get_availabilities(barber.id)
        return {'availability': availabilities}


class GetBarberServicesSerializer(BarberValidationMixin, serializers.Serializer):
    """
    Barber only: Returns all services for a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs
    
    def get_services(self, barber_id):
        services = Service.objects.filter(barber_id=barber_id)
        return [{'id': s.id, 'name': s.name, 'price': s.price} for s in services]

    def to_representation(self, validated_data):
        barber = validated_data['barber']
        services = self.get_services(barber.id)
        return {'services': services}


class CreateBarberServiceSerializer(BarberValidationMixin, ServiceValidationMixin, serializers.Serializer):
    """
    Barber only: Creates a new service for a given barber.
    """
    name = serializers.CharField(required=True, max_length=100)
    price = serializers.DecimalField(required=True, max_digits=6, decimal_places=2) 

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_service_name(attrs)
        return attrs

    def create(self, validated_data):
        return Service.objects.create(**validated_data)
    

class UpdateBarberServiceSerializer(BarberValidationMixin, FindServiceValidationMixin, ServiceValidationMixin, serializers.Serializer):
    """
    Barber only: Updates a given existing service, for a given barber.
    """
    name = serializers.CharField(required=False, max_length=100)
    price = serializers.DecimalField(required=False, max_digits=6, decimal_places=2)

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_find_service(attrs)

        if 'name' not in attrs and 'price' not in attrs:
            raise serializers.ValidationError('You must provide at least one field: name or price.')
        
        if 'name' in attrs:
            attrs = self.validate_service_name(attrs, service_instance=attrs['service'])
        
        return attrs

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.name = validated_data['name']

        if 'price' in validated_data:
            instance.price = validated_data['price']
            
        instance.save()
        return instance

    def save(self, **kwargs):
        return self.update(self.validated_data['service'], self.validated_data)


class DeleteBarberServiceSerializer(BarberValidationMixin, FindServiceValidationMixin, serializers.Serializer):
    """
    Barber only: Deletes a given service, for a given barber.
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_find_service(attrs)
        return attrs

    def delete(self):
        self.validated_data['service'].delete()


# TODO
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