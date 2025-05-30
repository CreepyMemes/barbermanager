from rest_framework import serializers
from ..models import Service



class AddServiceSerializer( serializers.Serializer):
    """
    Admin only: Invites a barber, accepts only email.
    """
    name = serializers.CharField(required=True)
    price = serializers.NumericField(required=True)
    barberId = serializers.CharField(required=True)

    def create(self, validated_data):
        name = validated_data.get('name')
        price = validated_data.get('price')
        barberId = validated_data.get('barberId')

        service = Service(
            barberId,
            name,
            price
        )
        service.save()

        return service
    

