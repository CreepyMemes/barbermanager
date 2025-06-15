from rest_framework import serializers
from ..utils import (
    BarberValidationMixin,
    ServiceValidationMixin,
    GetServicesMixin,
    GetReviewsMixin,
    GetAvailabilitiesMixin,
    GetAppointmentsMixin,
)
from ..models import (
    Service,
)


class GetBarberProfileSerializer(BarberValidationMixin, GetServicesMixin, GetReviewsMixin, serializers.Serializer):
    """
    Returns all the public information related to the profile of a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs
    
    def to_representation(self, validated_data):
        barber = validated_data['barber']
        services = self.get_services_barber(barber.id)
        reviews = self.get_reviews_barber(barber.id)
        return {
            'id': barber.id,
            'role': barber.role,
            'username': barber.username,
            'email': barber.email,
            'name': barber.name,
            'surname': barber.surname,
            'services': services,
            'reviews': reviews,
        }


class GetBarberAvailabilitiesSerializer(BarberValidationMixin, GetAvailabilitiesMixin, serializers.Serializer):
    """
    Barber only: Returns all availabilities for a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs
    
    
    def to_representation(self, validated_data):
        barber = validated_data['barber']
        availabilities = self.get_availabilities_barber(barber.id)
        return {'availability': availabilities}


class GetBarberServicesSerializer(BarberValidationMixin, GetServicesMixin, serializers.Serializer):
    """
    Barber only: Returns all services offered by a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs
    
    def to_representation(self, validated_data):
        barber = validated_data['barber']
        services = self.get_services_barber(barber.id)
        return {'services': services}


class CreateBarberServiceSerializer(BarberValidationMixin, ServiceValidationMixin, serializers.Serializer):
    """
    Barber only: Creates a new service offering for a given barber.
    """
    name = serializers.CharField(required=True, max_length=100)
    price = serializers.DecimalField(required=True, max_digits=6, decimal_places=2) 

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_service_name(attrs)
        return attrs

    def create(self, validated_data):
        return Service.objects.create(**validated_data)
    

class UpdateBarberServiceSerializer(BarberValidationMixin, ServiceValidationMixin, serializers.Serializer):
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


class DeleteBarberServiceSerializer(BarberValidationMixin, ServiceValidationMixin, serializers.Serializer):
    """
    Barber only: Deletes a given existing service, for a given barber.
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_find_service(attrs)
        return attrs

    def delete(self):
        self.validated_data['service'].delete()


class GeBarberAppointmentsSerializer(BarberValidationMixin, GetAppointmentsMixin, serializers.Serializer):
    """
    Barber only: Returns all ONGOING appointments for a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs

    def to_representation(self, validated_data):
        barber = validated_data['barber']
        appointments = self.get_appointments_barber(barber.id)
        return {'appointments': appointments}
    

class GetBarberReviewsSerializer(BarberValidationMixin, GetReviewsMixin, serializers.Serializer):
    """
    Barber only: Returns all reviews received by a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs

    def to_representation(self, validated_data):
        barber = validated_data['barber']
        reviews = self.get_reviews_barber(barber.id)
        return {'reviews': reviews}