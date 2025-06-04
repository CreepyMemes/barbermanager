from rest_framework import serializers
from ..utils import (
    BarberValidationMixin,
)
from ..models import (
    Service,
    Appointment,
)


class AddServiceSerializer(BarberValidationMixin, serializers.Serializer):
    """
    Admin only: Invites a barber, accepts only email.
    """
    name = serializers.CharField(required=True, max_length=100)
    price = serializers.DecimalField(required=True, max_digits=6, decimal_places=2) 

    def validate(self, attrs):
        attrs = self.validate_barber(attrs)

        barber = attrs['barber']
        name = attrs['name']

        if Service.objects.filter(barber=barber, name__iexact=name).exists():
            raise serializers.ValidationError(f'You already offer a service with the name: {name}.')
        
        return attrs

    def create(self, validated_data):
        return Service.objects.create(**validated_data)
    

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