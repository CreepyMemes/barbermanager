from django.utils import timezone
from rest_framework import serializers
from ..utils import (
    ClientValidationMixin,
    BarberValidationMixin,
    UsernameValidationMixin,
    AppointmentValidationMixin,
    ReviewValidationMixin,
    GetAppointmentsMixin,
    GetReviewsMixin,
    phone_number_validator,
)
from ..models import (
    Appointment, 
    Service, 
    Review,
    AppointmentStatus, 
)


class GetClientProfileSerializer(ClientValidationMixin, GetAppointmentsMixin, GetReviewsMixin, serializers.Serializer):
    """
    Returns all the information related the profile of a given client
    """
    def validate(self, attrs):
        attrs = self.validate_client(attrs)
        return attrs

    def to_representation(self, validated_data):
        client = validated_data['client']
        appointments = self.get_appointments_client(client.id)
        reviews = self.get_reviews_client(client.id)
        return {
            'id': client.id,
            'role': client.role,
            'username': client.username,
            'email': client.email,
            'phone_number': client.phone_number,
            'name': client.name,
            'surname': client.surname,
            'appointments': appointments,
            'reviews': reviews,  
        }


class UpdateClientProfileSerializer(ClientValidationMixin, UsernameValidationMixin, serializers.Serializer):
    """
    Client only: Updates general informations about a given client.
    """
    username = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    surname = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False, max_length=16, validators=[phone_number_validator])

    def validate(self, attrs):
        attrs = self.validate_client(attrs)

        if not any(field in attrs for field in ('username', 'name', 'surname', 'phone_number')):
            raise serializers.ValidationError('You must provide at least one field: username, name, surname or phone_number.')
        
        if 'username' in attrs:
            attrs = self.validate_username_unique(attrs, user_instance=attrs['client'])

        return attrs

    def update(self, instance, validated_data):
        if 'username' in validated_data:
            instance.username = validated_data['username']

        if 'name' in validated_data:
            instance.name = validated_data['name']
        
        if 'surname' in validated_data:
            instance.surname = validated_data['surname']
        
        if 'phone_number' in validated_data:
            instance.phone_number = validated_data['phone_number']

        instance.save()
        return instance

    def save(self, **kwargs):
        return self.update(self.validated_data['client'], self.validated_data)
    

class DeleteClientProfileSerializer(ClientValidationMixin, serializers.Serializer):
    """
    Client only: Deletes a given existing client account.
    """
    def validate(self, attrs):
        attrs = self.validate_client(attrs)
        return attrs

    def delete(self):
        self.validated_data['client'].delete()


class GetClientAppointmentsSerializer(ClientValidationMixin, GetAppointmentsMixin, serializers.Serializer):
    """
    Client only: Returns all appointments for a given client
    """
    def validate(self, attrs):
        attrs = self.validate_client(attrs)
        return attrs
    
    def to_representation(self, validated_data):
        client = validated_data['client']
        appointments = self.get_appointments_client(client.id)
        return {'appointments': appointments}
    

class CreateClientAppointmentSerializer(ClientValidationMixin, BarberValidationMixin, AppointmentValidationMixin, serializers.Serializer):
    """
    Client only: Creates a new appointment for a given client with a barber.
    """
    date = serializers.DateField(required=True)
    slot = serializers.TimeField(required=True)
    services = serializers.PrimaryKeyRelatedField(required=True, queryset=Service.objects.all(), many=True)

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        attrs = self.validate_client(attrs)
        attrs = self.validate_appointment_date_and_slot(attrs)
        attrs = self.validate_services_belong_to_barber(attrs)
        return attrs

    def create(self, validated_data):
        client = validated_data['client']
        barber = validated_data['barber']
        date = validated_data['date']
        slot = validated_data['slot']
        services = validated_data['services']

        appointment = Appointment(
            client=client, 
            barber=barber, 
            date=date, 
            slot=slot
        )
        appointment.save()
        appointment.services.set(services)

        return appointment
    

class CancelClientAppointmentSerializer(ClientValidationMixin, AppointmentValidationMixin, serializers.Serializer):
    """
    Client only: Cancels an ONGOING appointment for the authenticated client.
    """
    def validate(self, attrs):
        attrs = self.validate_client(attrs)
        attrs = self.validate_find_appointment(attrs)
        return attrs
    
    def save(self):
        appointment = self.validated_data['appointment']
        appointment.status = AppointmentStatus.CANCELLED.value
        appointment.save()

        return appointment


class GetClientReviewsSerializer(ClientValidationMixin, GetReviewsMixin, serializers.Serializer):
    """
    Client only: Returns all reviews posted by a given client
    """
    def validate(self, attrs):
        attrs = self.validate_client(attrs)
        return attrs

    def to_representation(self, validated_data):
        client = validated_data['client']
        reviews = self.get_reviews_client(client.id)
        return {'reviews': reviews}


class CreateClientReviewSerializer(ClientValidationMixin, ReviewValidationMixin, serializers.Serializer):
    """
    Client only: Creates a review post for a to the barber associated to the given client's COMPLETED appointment
    """
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(allow_blank=True, required=False, max_length=500)

    def validate(self, attrs):
        attrs = self.validate_client(attrs)
        attrs = self.validate_appointment_for_review(attrs)
        return attrs

    def create(self, validated_data):
        review = Review(
            appointment=validated_data['appointment'],
            client=validated_data['client'],
            barber=validated_data['barber'],
            rating=validated_data['rating'],
        )
        if 'comment' in validated_data:
            review.comment = validated_data['comment']

        review.save()

        return review
    

class UpdateClientReviewSerializer(ClientValidationMixin, ReviewValidationMixin, serializers.Serializer):
    """
    Client only: Updates a given existing review, for a given client.
    """
    rating = serializers.IntegerField(min_value=1, max_value=5, required=False)
    comment = serializers.CharField(allow_blank=True, required=False, max_length=500)

    def validate(self, attrs):
        attrs = self.validate_client(attrs)
        attrs = self.validate_find_review(attrs)

        if 'rating' not in attrs and 'comment' not in attrs:
            raise serializers.ValidationError('You must provide at least one field to update: rating or comment.')
        
        return attrs

    def update(self, instance, validated_data):
        if 'rating' in validated_data:
            instance.rating = validated_data['rating']
            updated = True

        if 'comment' in validated_data:
            instance.comment = validated_data['comment']
            updated = True

        if updated:
            instance.edited_at = timezone.now()

        instance.save()

        return instance

    def save(self, **kwargs):
        return self.update(self.validated_data['review'], self.validated_data)


class DeleteClientReviewSerializer(ClientValidationMixin, ReviewValidationMixin, serializers.Serializer):
    """
    Client only: Deletes a given existing reveiw, for a given client.
    """
    def validate(self, attrs):
        attrs = self.validate_client(attrs)
        attrs = self.validate_find_review(attrs)
        return attrs

    def delete(self):
        self.validated_data['review'].delete()

