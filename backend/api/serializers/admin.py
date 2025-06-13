from django.db.models import Sum, Avg
from rest_framework import serializers
from ..utils import (
    EmailValidationMixin,
    BarberValidationMixin,
    AvailabilityValidationMixin,
)
from ..models import(
    Barber,
    Availability,
    Appointment,
    Review,
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

        
class GetAdminStatisticsSerializer(serializers.Serializer):
    """
    Admin only: Returns general statistics counts, revenue, and average rating. 
    """
    def get_total_appointments(self):
        return Appointment.objects.count()
    
    def get_total_revenue(self):
        revenue = (
            Appointment.objects.filter(status="COMPLETED")
            .annotate(price_sum=Sum('services__price'))
            .aggregate(total=Sum('price_sum'))['total']
        )
        return revenue or 0
    
    def get_total_reviews(self):
        return Review.objects.count()
    
    def get_average_rating(self):
        avg = Review.objects.aggregate(avg=Avg('rating'))['avg']
        return round(avg or 0.0, 2)
    
    def to_representation(self, instance):
        return {
            'statistics': {
                'total_appointments': self.get_total_appointments(),
                'total_revenue': self.get_total_revenue(),
                'total_reviews': self.get_total_reviews(),
                'average_rating': self.get_average_rating(),
            }
        }

      
class GetAllAppointmentsSerializer(serializers.Serializer):
    """
    Admin only: Returns all appointments registered in the system
    """
    def get_appointments(self):
        appointments = Appointment.objects.all()
        return [{
            'id': a.id, 
            'client_id': a.client.id, 
            'barber_id': a.barber.id, 
            'date': a.date, 
            'slot': a.slot.strftime("%H:%M"), 
            'services': [s.id for s in a.services.all()], 
            'status': a.status,
            'reminder_email_sent': a.reminder_email_sent,
        } for a in appointments]

    def to_representation(self, validated_data):
        appointments = self.get_appointments()
        return {'appointments': appointments}
