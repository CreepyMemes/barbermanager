from rest_framework import serializers
from ..utils import(
    BarberValidationMixin,
    ClientValidationMixin,
    GetBarbersMixin,
    GetClientsMixin,
)


class GetBarbersPublicSerializer(GetBarbersMixin, serializers.Serializer):
    """
    Returns all barbers registered and their public data 
    """
    def to_representation(self, instance):
        return {'barbers': self.get_barbers_public()}


class GetBarberProfilePublicSerializer(BarberValidationMixin, GetBarbersMixin, serializers.Serializer):
    """
    Returns all the public information related to the profile of a given barber
    """
    def validate(self, attrs):
        attrs = self.validate_barber(attrs)
        return attrs
    
    def to_representation(self, validated_data):
        barber = validated_data['barber']
        return {'profile': self.get_barber_public(barber)}
    

class GetClientProfilePublicSerializer(ClientValidationMixin, GetClientsMixin, serializers.Serializer):
    """
    Returns all the public information related to the profile of a given client
    """
    def validate(self, attrs):
        attrs = self.validate_client(attrs)
        return attrs
    
    def to_representation(self, validated_data):
        client = validated_data['client']
        return {'profile': self.get_client_public(client)}