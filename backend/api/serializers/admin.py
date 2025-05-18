from rest_framework import serializers
from ..models import Barber
from ..utils import EmailValidationMixin


class BarberInviteSerializer(EmailValidationMixin, serializers.Serializer):
    """
    Admin only: Invites a barber, accepts only email.
    """
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        email = validated_data.get('email')

        barber = Barber(
            email=email,
            is_active=False
        )
        barber.set_unusable_password()
        barber.save()

        return barber