import uuid
from rest_framework import serializers
from ..utils import (
    AdminValidationMixin,
    EmailValidationMixin,
    BarberValidationMixin,
    AvailabilityValidationMixin,
    GetAdminsMixin,
    GetAppointmentsMixin,
    GetBarbersMixin,
    GetClientsMixin,
)
from ..models import(
    Barber,
    Availability,
)


class GetAdminProfileSerializer(AdminValidationMixin, GetAdminsMixin, serializers.Serializer):
    """
    Returns all the information related the profile of a given admin
    """
    def validate(self, attrs):
        attrs = self.validate_admin(attrs)
        return attrs

    def to_representation(self, validated_data):
        admin = validated_data['admin']
        return {'profile': self.get_admin_private(admin) }


class GetAllBarbersSerializer(GetBarbersMixin, serializers.Serializer):
    """
    Returns all barbers registered and their data 
    """
    def to_representation(self, instance):
        return {'barbers': self.get_barbers_private(show_all=True)}


class GetAllClientsSerializer(GetClientsMixin, serializers.Serializer):
    """
    Returns all clients registered and their data 
    """
    def to_representation(self, instance):
        return {'clients': self.get_clients_private(show_all=True)}


class GetAllAppointmentsSerializer(GetAppointmentsMixin, serializers.Serializer):
    """
    Admin only: Returns all appointments registered in the system
    """
    def to_representation(self, instance):
        return {'appointments': self.get_appointments_public(show_all=True)}
    

class InviteBarberSerializer(EmailValidationMixin, serializers.Serializer):
    """
    Admin only: Invites a barber, accepts only email.
    """
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        attrs = self.validate_email_unique(attrs)
        return attrs

    def create(self, validated_data):
        barber = Barber(
            email=validated_data['email'],
            username=f'b_{str(uuid.uuid4())[:8]}', # first 8 chars of UUID (e.g. 'b_d3a7f601')
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

        return value
    
    def delete(self):
        self.barber.delete()
        return self.barber
    

class CreateBarberAvailabilitySerializer(BarberValidationMixin, AvailabilityValidationMixin, serializers.Serializer):
    """
    Admin only: Creates a barber's availability for a specific date.
    """
    date = serializers.DateField(required=True)
    slots = serializers.ListField(required=True, child=serializers.TimeField(required=True), min_length=1)

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_availability_date(attrs)
        return attrs

    def create(self, validated_data):
        validated_data["slots"] = [slot.strftime("%H:%M") for slot in validated_data["slots"]]
        return Availability.objects.create(**validated_data)


class UpdateBarberAvailabilitySerializer(BarberValidationMixin, AvailabilityValidationMixin, serializers.Serializer):
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
    

class DeleteBarberAvailabilitySerializer(BarberValidationMixin, AvailabilityValidationMixin, serializers.Serializer):
    """
    Admin only: Deletes a given availability, for a given barber.
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_find_availability(attrs)
        return attrs

    def delete(self):
        self.validated_data['availability'].delete()

