from rest_framework import serializers
from api.models.appointment import Appointment, AppointmentStatus, Service, Review


# 🔹 Serializer per visualizzare appuntamenti passati
class AppointmentSerializer(serializers.ModelSerializer):
    services = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    barber_email = serializers.EmailField(source='barber.email', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'barber_email', 'date', 'slot', 'services', 'status']


# 🔹 Serializer per creare nuovi appuntamenti
class AppointmentCreateSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)

    class Meta:
        model = Appointment
        fields = ['barber', 'date', 'slot', 'services']

    def validate(self, attrs):
        barber = attrs['barber']
        date = attrs['date']
        slot = attrs['slot']

        if Appointment.objects.filter(barber=barber, date=date, slot=slot).exists():
            raise serializers.ValidationError("This slot is already booked.")

        for service in attrs['services']:
            if service.barber != barber:
                raise serializers.ValidationError(f"The service '{service.name}' is not offered by this barber.")
        
        return attrs

    def create(self, validated_data):
        client = self.context['client']
        services = validated_data.pop('services')
        appointment = Appointment.objects.create(client=client, status=AppointmentStatus.ONGOING.value, **validated_data)
        appointment.services.set(services)
        return appointment


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
