from rest_framework import serializers
from ..utils import (
    EmailValidationMixin,
    BarberValidationMixin,
    AvailabilityValidationMixin,
    FindAvailabilityValidationMixin,
)
from ..models import(
    Barber,
    Availability,
)


class InviteBarberSerializer(EmailValidationMixin, serializers.Serializer):
    """
    Admin only: Invites a barber, accepts only email.
    """
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        barber = Barber(email=validated_data['email'],is_active=False)
        barber.set_unusable_password()
        barber.save()

        return barber
    

class DeleteBarberSerializer(serializers.Serializer):
    """
    Admin only: Deletes a barber by ID if they exist
    """
    id = serializers.IntegerField(required=True)

    def validate_id(self, value):

        try:
            self.barber = Barber.objects.get(id=value)
        except Barber.DoesNotExist:
            raise serializers.ValidationError("Barber with this ID does not exist.")  
        
        if not self.barber.is_active:
            raise serializers.ValidationError("Barber is not active and cannot be deleted.")
        
        return value
    
    def delete(self):
        self.barber.delete()
        return self.barber
    

class CreateBarberAvailabilitySerializer(BarberValidationMixin, AvailabilityValidationMixin, serializers.Serializer):
    """
    Admin only: Creates a barber's availability for a specific date.
    """
    date = serializers.DateField(required=True)
    slots = serializers.ListField(required=True, child=serializers.RegexField(r'^\d\d:\d\d$', required=True), min_length=1)

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_availability_date(attrs)
        return attrs

    def create(self, validated_data):
        return Availability.objects.create(**validated_data)


class UpdateBarberAvailabilitySerializer(BarberValidationMixin, FindAvailabilityValidationMixin, AvailabilityValidationMixin, serializers.Serializer):
    """
    Admin only: Updates a given existing availability, for a given barber.
    """
    date = serializers.DateField(required=False)
    slots = serializers.ListField(required=False, child=serializers.RegexField(r'^\d\d:\d\d$'), min_length=1)

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_find_availability(attrs)

        if 'date' not in attrs and 'slots' not in attrs:
            raise serializers.ValidationError('You must provide at least one field: date or slots.')
        
        if 'date' in attrs:
            attrs = self.validate_availability_date(attrs, availability_instance=attrs['availability'])

        return attrs

    def update(self, instance, validated_data):
        if 'date' in validated_data:
            instance.date = validated_data['date']

        if 'slots' in validated_data:
            instance.slots = validated_data['slots']

        instance.save()
        return instance

    def save(self, **kwargs):
        return self.update(self.validated_data['availability'], self.validated_data)
    

class DeleteBarberAvailabilitySerializer(BarberValidationMixin, FindAvailabilityValidationMixin, serializers.Serializer):
    """
    Admin only: Deletes a given availability, for a given barber.
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_find_availability(attrs)
        return attrs

    def delete(self):
        self.validated_data['availability'].delete()


class AdminStatisticsSerializer(serializers.Serializer):
    total_appointments = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_reviews = serializers.IntegerField()
    average_rating = serializers.FloatField()