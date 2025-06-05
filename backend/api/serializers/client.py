from rest_framework import serializers
from ..utils import (
    ClientValidationMixin,
    BarberValidationMixin,
    AppointmentValidationMixin,
)
from ..models import (
    Appointment, 
    Service, 
    Review,
    AppointmentStatus, 
)


class GetAppointmentsSerializer(ClientValidationMixin, serializers.Serializer):
    """
    Client only: Returns all appointments for a given client
    """
    def validate(self, attrs):
        attrs = self.validate_client(attrs)
        return attrs
    
    def get_appointments(self, client_id):
        appointments = Appointment.objects.filter(client_id=client_id)
        return [{'id': a.id, 'barber_id': a.barber.id, 'date': a.date, 'slot': a.slot, 'services': [s.id for s in a.services.all()], 'status': a.status} for a in appointments]

    def to_representation(self, validated_data):
        client = validated_data['client']
        appointments = self.get_appointments(client.id)
        return {'appointments': appointments}
    

class CreateAppointmentSerializer(ClientValidationMixin, BarberValidationMixin, AppointmentValidationMixin, serializers.Serializer):
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

        appointment = Appointment.objects.create(client=client, barber=barber, date=date, slot=slot)
        appointment.services.set(services)
        return appointment
    
    
# class CreateAppointmentSerializer(serializers.ModelSerializer):
#     """
#     Client only: Creates a new appointment for a given client
#     """
#     services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)

#     class Meta:
#         model = Appointment
#         fields = ['barber', 'date', 'slot', 'services']

#     def validate(self, attrs):
#         barber = attrs['barber']
#         date = attrs['date']
#         slot = attrs['slot']

#         if Appointment.objects.filter(barber=barber, date=date, slot=slot).exists():
#             raise serializers.ValidationError("This slot is already booked.")

#         for service in attrs['services']:
#             if service.barber != barber:
#                 raise serializers.ValidationError(f"The service '{service.name}' is not offered by this barber.")
        
#         return attrs

#     def create(self, validated_data):
#         client = self.context['client']
#         services = validated_data.pop('services')
#         appointment = Appointment.objects.create(client=client, status=AppointmentStatus.ONGOING.value, **validated_data)
#         appointment.services.set(services)
#         return appointment


# 🔹 Serializer per creare/modificare una review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'appointment', 'barber', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        user = self.context['request'].user
        appointment = data.get('appointment')

        if appointment.client != user:
            raise serializers.ValidationError("This appointment does not belong to you.")

        if appointment.status != AppointmentStatus.COMPLETED.value:
            raise serializers.ValidationError("You can only review a completed appointment.")

        if Review.objects.filter(client=user, barber=appointment.barber).exists():
            raise serializers.ValidationError("You have already reviewed this barber.")

        return data

    def create(self, validated_data):
        validated_data['barber'] = validated_data['appointment'].barber
        return super().create(validated_data)
