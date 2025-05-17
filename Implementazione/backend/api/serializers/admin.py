from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Barber


User = get_user_model()


class BarberInviteSerializer(serializers.Serializer):
    """
    Admin only: Invites a barber, accepts only email.
    """
    email = serializers.EmailField()

    class Meta:
        model = Barber
        fields = ['email']
    

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        return email
    

    def create(self, validated_data):
        email = validated_data.get('email')

        barber = Barber(
            email=email,
            is_active=False
        )
        barber.set_unusable_password()
        barber.save()

        return barber