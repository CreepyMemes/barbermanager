from rest_framework import serializers
from ..utils import (
    BarberValidationMixin,
    UsernameValidationMixin,
    ServiceValidationMixin,
    GetBarbersMixin,
    GetAvailabilitiesMixin,
    GetServicesMixin,
    GetAppointmentsMixin,
    GetReviewsMixin,
)
from ..models import (
    Service,
)


class GetBarberProfileSerializer(BarberValidationMixin, GetBarbersMixin, serializers.Serializer):
    """
    Returns all the public information related to the profile of a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs
    
    def to_representation(self, validated_data):
        barber = validated_data['barber']
        return {'profile': self.get_barber_private(barber)}


class UpdateBarberProfileSerializer(BarberValidationMixin, UsernameValidationMixin, serializers.Serializer):
    """
    Barber only: Updates general informations about a given barber.
    """
    username = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    surname = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)

        if not any(field in attrs for field in ('username', 'name', 'surname', 'description')):
            raise serializers.ValidationError('You must provide at least one field: username, name, surname or description.')
        
        if 'username' in attrs:
            attrs = self.validate_username_unique(attrs, user_instance=attrs['barber'])

        return attrs

    def update(self, instance, validated_data):
        if 'username' in validated_data:
            instance.username = validated_data['username']

        if 'name' in validated_data:
            instance.name = validated_data['name']
        
        if 'surname' in validated_data:
            instance.surname = validated_data['surname']
        
        if 'description' in validated_data:
            instance.description = validated_data['description']

        instance.save()
        return instance

    def save(self, **kwargs):
        return self.update(self.validated_data['barber'], self.validated_data)
    

class DeleteBarberProfileSerializer(BarberValidationMixin, serializers.Serializer):
    """
    Barber only: Deletes a given existing barber account.
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs

    def delete(self):
        self.validated_data['barber'].delete()


class GetBarberAvailabilitiesSerializer(BarberValidationMixin, GetAvailabilitiesMixin, serializers.Serializer):
    """
    Barber only: Returns all availabilities for a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs
    
    def to_representation(self, validated_data):
        barber = validated_data['barber']
        return {'availabilities': self.get_availabilities_public(barber.id)}


class GetBarberSlotsSerializer(BarberValidationMixin, GetAvailabilitiesMixin, serializers.Serializer):
    """
    Barber only: Returns all slots for a given barber and date
    """
    date = serializers.DateField(required=True)

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs

    def to_representation(self, validated_data):
        barber = validated_data['barber']
        date = validated_data['date']

        from ..models import Availability

        # Find the matching availability instance for the barber and date
        try:
            availability = Availability.objects.get(barber=barber, date=date)
        except Availability.DoesNotExist:
            return {"slots": []}

        # Optionally filter slots if date is today
        slots = self._filter_slots_future(availability)
        return {"slots": slots}


class GetBarberServicesSerializer(BarberValidationMixin, GetServicesMixin, serializers.Serializer):
    """
    Barber only: Returns all services offered by a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs
    
    def to_representation(self, validated_data):
        barber = validated_data['barber']
        return {'services': self.get_services_public(barber.id)}


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

        if not any(field in attrs for field in ('name', 'price')):
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
    Barber only: Returns all appointments for a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs

    def to_representation(self, validated_data):
        barber = validated_data['barber']
        return {'appointments': self.get_appointments_public(barber_id=barber.id)}
    

class GetBarberReviewsSerializer(BarberValidationMixin, GetReviewsMixin, serializers.Serializer):
    """
    Barber only: Returns all reviews received by a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs

    def to_representation(self, validated_data):
        barber = validated_data['barber']
        return {'reviews': self.get_reviews_public(barber_id=barber.id)}