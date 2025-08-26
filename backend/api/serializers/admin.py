import uuid
from datetime import timedelta, datetime
from rest_framework import serializers
from ..utils import (
    AdminValidationMixin,
    UsernameValidationMixin,
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


class UpdateAdminProfileSerializer(AdminValidationMixin, UsernameValidationMixin, serializers.Serializer):
    """
    Admin only: Updates general informations about a given admin.
    """
    username = serializers.CharField(required=False)

    def validate(self, attrs):
        attrs = self.validate_admin(attrs)

        if not any(field in attrs for field in ['username']):
            raise serializers.ValidationError('You must provide at least one field: username.')
        
        if 'username' in attrs:
            attrs = self.validate_username_unique(attrs, user_instance=attrs['admin'])

        return attrs

    def update(self, instance, validated_data):
        if 'username' in validated_data:
            instance.username = validated_data['username']

        instance.save()
        return instance

    def save(self, **kwargs):
        return self.update(self.validated_data['admin'], self.validated_data)
    

class DeleteAdminProfileSerializer(AdminValidationMixin, serializers.Serializer):
    """
    Admin only: Deletes a given existing admin account.
    """
    def validate(self, attrs):
        attrs = self.validate_admin(attrs)
        return attrs

    def delete(self):
        self.validated_data['admin'].delete()


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
    Admin only: Create a barber's availability for a date range (or a single day).

    - start_date    (REQUIRED): first date (YYYY-MM-DD)
    - end_date      (OPTIONAL): last date (YYYY-MM-DD), use start_date if omitted
    - start_time    (REQUIRED): slot window (HH:MM)
    - end_time      (REQUIRED): slot window (HH:MM)
    - slot_interval (OPTIONAL): slot length in minutes (default 30)
    - days_of_week  (OPTIONAL): list [0=Mon...6=Sun], used only if multiple days
    """
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=False)
    start_time = serializers.TimeField(required=True)
    end_time = serializers.TimeField(required=True)
    slot_interval = serializers.IntegerField(required=False, min_value=1, default=30)
    days_of_week = serializers.ListField(required=False, allow_null=True, allow_empty=True, child=serializers.IntegerField(min_value=0, max_value=6))

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)

        start_date = attrs['start_date']
        end_date = attrs.get('end_date', start_date) # Defaults back to start_date if omitted

        if end_date < start_date:
            raise serializers.ValidationError("end_date cannot be before start_date")
        
        attrs['end_date'] = end_date  # ensure always present and >= start
        attrs['slot_interval'] = attrs.get('slot_interval', 30)

        return attrs
    
    def create(self, validated_data):
        barber = validated_data['barber']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']
        interval = validated_data['slot_interval']
        days_of_week = validated_data.get('days_of_week')

        # Single day mode, ignores days_of_week
        if start_date == end_date:
            target_dates = [start_date]

        # Multi day mode, filters by days_of_week if provided
        else:
            span = (end_date - start_date).days + 1
            raw_dates = [start_date + timedelta(days=days) for days in range(span)]

            if days_of_week:
                target_dates = [day for day in raw_dates if day.weekday() in days_of_week]
            else:
                target_dates = raw_dates

        availabilities = []
        for date in target_dates:
            slots = self.generate_slots(start_time, end_time, interval)

            if not slots:
                continue

            # Uniqueness enforced by update_or_create (overwrite for admin)
            availability, _created = Availability.objects.update_or_create(
                barber=barber,
                date=date,
                defaults={"slots": slots}
            )
            availabilities.append(availability)

        return availabilities


class UpdateBarberAvailabilitySerializer(BarberValidationMixin, AvailabilityValidationMixin, serializers.Serializer):
    """
    Admin only: Update slots for an existing availability by providing a new start/end time and optional interval.
    """
    start_time = serializers.TimeField(required=True)
    end_time = serializers.TimeField(required=True)
    slot_interval = serializers.IntegerField(required=False, min_value=1, default=30)

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_find_availability(attrs)
        attrs['slot_interval'] = attrs.get('slot_interval', 30)
        return attrs

    def update(self, instance, validated_data):
        slots = self.generate_slots(validated_data['start_time'], validated_data['end_time'], validated_data['slot_interval'])
        
        if not slots:
            raise serializers.ValidationError('No valid slots produced; check start_time, end_time, and interval.')

        instance.slots = slots
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

