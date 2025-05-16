from rest_framework import serializers

class BarberInviteSerializer(serializers.Serializer):
    """
    Invite a barber: accept only email.
    """
    email = serializers.EmailField()