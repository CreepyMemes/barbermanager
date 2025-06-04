from rest_framework import serializers
from ..utils import (
    BarberValidationMixin,
)
from ..models import Service
from ..models import Appointment


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'price']

    def validate(self, attrs):
        barber = self.context['barber']
        name = attrs.get('name', self.instance.name if self.instance else None)

        qs = Service.objects.filter(barber=barber, name__iexact=name)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError(f'You already offer a service with the name: {name}.')

        self.barber = barber
        return attrs

    def create(self, validated_data):
        return Service.objects.create(barber=self.barber, **validated_data)


class AppointmentSerializer(serializers.ModelSerializer):
    client_email = serializers.CharField(source='client.email', read_only=True)
    services = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Appointment
        fields = ['id', 'client_email', 'date', 'slot', 'services', 'status']