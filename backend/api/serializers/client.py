from django.utils import timezone
from rest_framework import serializers
from ..utils import (
    ClientValidationMixin,
    BarberValidationMixin,
    AppointmentValidationMixin,
    ReviewValidationMixin,
)
from ..models import (
    Appointment, 
    Service, 
    Review,
    AppointmentStatus, 
)


class GetClientAppointmentsSerializer(ClientValidationMixin, serializers.Serializer):
    """
    Client only: Returns all appointments for a given client
    """
    def validate(self, attrs):
        attrs = self.validate_client(attrs)
        return attrs
    
    def get_appointments(self, client_id):
        appointments = Appointment.objects.filter(client_id=client_id)
        return [{
            'id': a.id, 
            'barber_id': a.barber.id, 
            'date': a.date, 
            'slot': a.slot.strftime("%H:%M"), 
            'services': [s.id for s in a.services.all()], 
            'status': a.status
        } for a in appointments]

    def to_representation(self, validated_data):
        client = validated_data['client']
        appointments = self.get_appointments(client.id)
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

        appointment = Appointment.objects.create(client=client, barber=barber, date=date, slot=slot) # Default ONGOING status
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


class GetClientReviewsSerializer(ClientValidationMixin, serializers.Serializer):
    """
    Client only: Returns all reviews posted by a given client
    """
    def validate(self, attrs):
        attrs = self.validate_client(attrs)
        return attrs

    def get_reviews(self, client):
        reviews = Review.objects.filter(client=client).select_related('barber', 'appointment')
        return [{
            'id': r.id,
            'appointment_id': r.appointment.id,
            'barber_id': r.barber.id,
            'rating': r.rating,
            'comment': r.comment,
            'created_at': r.created_at.strftime('%Y-%m-%d'),
            'edited_at': r.edited_at.strftime('%Y-%m-%d') if r.edited_at else None
        } for r in reviews]

    def to_representation(self, validated_data):
        reviews = self.get_reviews(validated_data['client'])
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
        review = Review.objects.create(
            appointment=validated_data['appointment'],
            client=validated_data['client'],
            barber=validated_data['barber'],
            rating=validated_data['rating'],
            comment=validated_data.get('comment') # Not required
        )
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

