from rest_framework import serializers
from ..models import Barber
from ..utils import EmailValidationMixin


class InviteBarberSerializer(EmailValidationMixin, serializers.Serializer):
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