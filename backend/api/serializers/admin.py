from rest_framework import serializers
from ..utils import (
    EmailValidationMixin,
    BarberValidationMixin,
    NewAvailabilityValidationMixin,
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
        email = validated_data.get('email')

        barber = Barber(
            email=email,
            is_active=False
        )
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
    

class CreateBarberAvailabilitySerializer(BarberValidationMixin, NewAvailabilityValidationMixin, serializers.Serializer):
    """
    Admin only: Creates a barber's availability for a specific date.
    """
    date = serializers.DateField(required=True)
    slots = serializers.ListField(child=serializers.RegexField(r'^\d\d:\d\d$', required=True), min_length=1)

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_new_date(attrs)
        return attrs

    def create(self, validated_data):
        barber = validated_data['barber']
        date = validated_data['date']
        slots = validated_data['slots']

        return Availability.objects.create(
            barber=barber,
            date=date,
            slots=slots
        )


class UpdateBarberAvailabilitySerializer(BarberValidationMixin, FindAvailabilityValidationMixin, serializers.Serializer):
    """
    Admin only: Updates the slots of an existing barber's availability for a specific date.
    """
    date = serializers.DateField(required=True)
    slots = serializers.ListField(child=serializers.RegexField(r'^\d\d:\d\d$', required=True), min_length=1)

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_find_date(attrs)
        return attrs

    def update(self, instance, validated_data):
        slots = validated_data['slots']
        instance.slots = slots
        instance.save()
        return instance

    def save(self, **kwargs):
        return self.update(self.validated_data['availability'], self.validated_data)
    

class DeleteBarberAvailabilitySerializer(BarberValidationMixin, FindAvailabilityValidationMixin, serializers.Serializer):
    """
    Admin only: Deletes a barber's availability for a specific date.
    """
    date = serializers.DateField(required=True)

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_find_date(attrs)
        return attrs

    def delete(self):
        self.validated_data['availability'].delete()