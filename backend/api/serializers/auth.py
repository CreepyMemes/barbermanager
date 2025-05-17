from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Client, Barber


User = get_user_model()


class ClientRegisterSerializer(serializers.ModelSerializer):
    """
    Register a client. Sends a confirmation email.
    Client must provide valid username and password
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = Client
        fields = ['email', 'username', 'password']

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username is already taken.")
        
        return username
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        return email


    def validate_password(self, value):
        validate_password(value)
        return value


    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        password = validated_data.get('password')
    
        client = Client(
            email=email,
            username=username,
            is_active=False,
        )
        client.set_password(password)
        client.save()

        return client


class BarberRegisterSerializer(serializers.Serializer):
    """
    Barber completes registration via invite link. Only sets username and password.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Barber
        fields = ['username', 'password']


    def validate_password(self, value):
        validate_password(value)
        return value


    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username is already taken.")
        return username


    def create(self, validated_data):
        password = validated_data.get('password')
        username = validated_data.get('username')

        barber = self.context['barber']
        barber.username = username
        barber.set_password(password)
        barber.is_active = True
        barber.save()

        return barber
    

class LoginSerializer(serializers.Serializer):
    """
    Login using either email or username, not both.
    """
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if not email and not username:
            raise serializers.ValidationError({"error": "You must provide either an email or username."})
        if email and username:
            raise serializers.ValidationError({"error": "Provide only one of email or username, not both."})

        return data