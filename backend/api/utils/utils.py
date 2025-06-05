from django.urls import reverse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import  force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from ..models import (
    User, 
    Client,
    Barber,
    Appointment,
    Availability,
    Service,
)


def send_client_verify_email(email, uid, token, domain):
    """
    Sends email confirmation link to client after registration.
    """
    path = reverse('verify_client_email', kwargs={'uidb64': uid, 'token': token})
    link = f'{domain}{path}'

    subject = '[BarberManager] Verify your email to register as a client'
    message = (
        f'Thank you for registering.\n\n'
        f'Please click the link below to verify your account:\n'
        f'{link}\n\n'
        'If you did not register, please ignore this email.'
    )
    send_mail(subject, message, 'barber.manager.verify@gmail.com', [email])


def send_barber_invite_email(email, uid, token, domain):
    """
    Sends barber invitation email with registration link.
    """
    path = reverse('register_barber', kwargs={'uidb64': uid, 'token': token})
    link = f'{domain}{path}'

    subject = '[BarberManager] You have been invited to register as a barber'
    message = (
        f'You have been invited to join as a barber.\n\n'
        f'Please click the link below to complete your registration:\n'
        f'{link}\n\n'
        'If you did not expect this invitation, please ignore this email.'
    )
    send_mail(subject, message, 'barber.manager.verify@gmail.com', [email])


def send_password_reset_email(email, uid, token, domain):
    """
    Sends password reset email with reset link.
    """
    path = reverse('confirm_password_reset', kwargs={'uidb64': uid, 'token': token})
    link = f'{domain}{path}'

    subject = '[BarberManager] You have requested to reset your password'
    message = (
        f'We received a request to reset your password.\n\n'
        f'Please click the link below to set a new password:\n'
        f'{link}\n\n'
        'If you did not request a password reset, please ignore this email.'
    )
    send_mail(subject, message, 'barber.manager.verify@gmail.com', [email])


def get_user_from_uid_token(uidb64, token, role=None):
    """
    Utility function that checks if a token previously registered to a user is valid.
    Raises serializers.ValidationError if invalid.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        if role:
            user = User.objects.get(pk=uid, role=role)
        else:
            user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise serializers.ValidationError("Invalid link.")
    
    if not default_token_generator.check_token(user, token):
        raise serializers.ValidationError("Invalid or expired token.")

    return user


class PasswordValidationMixin:
    """
    Utility mixin to handle common password validation checks
    """
    def validate_password(self, value):
        validate_password(value)
        return value
    

class EmailValidationMixin:
    """
    Utility mixin to handle common email validation checks
    """
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(f'The email "{email}" is already taken.')
        return email


class UsernameValidationMixin:
    """
    Utility mixin to handle common username validation checks
    """
    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(f'The username "{username}" is already taken.')
        return username


class UIDTokenValidationSerializer(serializers.Serializer):
    """
    Utility serializer that handlles token checks, from which other serializers inherit
    """
    def validate_uid_token(self):
        uidb64 = self.context.get('uidb64')
        token = self.context.get('token')

        if not uidb64 or not token:
            raise serializers.ValidationError("Missing uid or token.")

        user = get_user_from_uid_token(uidb64, token)
        return user

    def validate(self, attrs):
        user = self.validate_uid_token()
        attrs['user'] = user
        return attrs
    

class ClientValidationMixin:
    """
    Mixin to validate that a client_id from context exists and is active. Also adds 'client' to attrs.
    """
    def validate_client(self, attrs):
        client_id = self.context.get('client_id')

        try:
            client = Client.objects.get(pk=client_id, is_active=True)
        except Client.DoesNotExist:
            raise serializers.ValidationError(f'Client with ID: "{client_id}" does not exist or is inactive.')
        
        attrs['client'] = client
        return attrs
    

class AppointmentValidationMixin:
    """
    Mixin that ensures the client doesn't already have an appointment with the same date, (same check with barber), 
    checks if availability for the given barber exists and the given slot exists in the given availability
    """
    def validate_services_belong_to_barber(self, attrs):
        barber = attrs['barber']
        services = attrs['services']

        for service in services:
            if service.barber_id != barber.id:
                raise serializers.ValidationError(f'Service with ID"{service.id}" for the barber "{barber}" does not exist.')
            
        return attrs

    def validate_appointment_date_and_slot(self, attrs):
        client = attrs['client']
        barber = attrs['barber']
        appointment_date = attrs['date']
        appointment_slot = attrs['slot']
    
        if Appointment.objects.filter(client=client, date=appointment_date).exists():
            raise serializers.ValidationError(f"Appointment for the date {appointment_date} for the client: {client} already existts.")

        if Appointment.objects.filter(barber=barber, date=appointment_date, slot=appointment_slot).exists():
            raise serializers.ValidationError(f"Appointment for the date: {appointment_date} in the slot: {appointment_slot} for the barber: {barber} already exists.")

        try:
            availability = Availability.objects.get(barber=barber, date=appointment_date)
        except Availability.DoesNotExist:
            raise serializers.ValidationError(f"Barber is not available on {appointment_date}.")
        
        slot_str = appointment_slot.strftime("%H:%M")

        if slot_str not in availability.slots:
            raise serializers.ValidationError(f"The Barber: {barber} is not available at {slot_str} on {appointment_date}.")

        return attrs
    
    

class BarberValidationMixin:
    """
    Mixin to validate that a barber_id from context exists and is active. Also adds 'barber' to attrs.
    """
    def validate_barber(self, attrs):
        barber_id = self.context.get('barber_id')

        try:
            barber = Barber.objects.get(pk=barber_id, is_active=True)
        except Barber.DoesNotExist:
            raise serializers.ValidationError(f'Barber with ID: "{barber_id}" does not exist or is inactive.')
        
        attrs['barber'] = barber
        return attrs


class AvailabilityValidationMixin:
    """
    Mixin that ensures the barber doesn't already have an availability with the same date.
    """
    def validate_availability_date(self, attrs, availability_instance=None):
        barber = attrs['barber']
        availability_date = attrs['date']

        availability =  Availability.objects.filter(barber=barber, date=availability_date)

        if availability_instance:
            availability = availability.exclude(pk=availability_instance.pk)

        if availability.exists():
            raise serializers.ValidationError(f'Availability with the date: "{availability_date}" for the barber: "{barber}" already exists.')

        return attrs


class FindAvailabilityValidationMixin:
    """
    Mixin to validate if the given date for the specific barber has an existing availabililty
    """
    def validate_find_availability(self, attrs):
        barber = attrs['barber']
        availability_id = self.context.get('availability_id')

        try:
            availability = Availability.objects.get(barber=barber, pk=availability_id)
        except Availability.DoesNotExist:
            raise serializers.ValidationError(f'Availability with the ID: "{availability_id}" for the barber: "{barber}" does not exist.')
        
        attrs['availability'] = availability
        return attrs
    

class ServiceValidationMixin:
    """
    Mixin that ensures the barber doesn't already have a service with the same name (case-insensitive).
    """
    def validate_service_name(self, attrs, service_instance=None):
        barber = attrs['barber']
        service_name = attrs['name']

        service = Service.objects.filter(barber=barber, name__iexact=service_name)

        if service_instance:
            service = service.exclude(pk=service_instance.pk)

        if service.exists():
            raise serializers.ValidationError(f'Service with the name: "{service_name}" for the barber: "{barber}" already exists.')
        
        return attrs


class FindServiceValidationMixin:
    """
    Mixin to validate a service belonging to the given barber by service_id from context.
    """
    def validate_find_service(self, attrs):
        barber = attrs['barber']
        service_id = self.context.get('service_id')

        try:
            service = Service.objects.get(barber=barber, pk=service_id)
        except Service.DoesNotExist:
            raise serializers.ValidationError(f'Service with the ID: "{service_id}" for the barber: "{barber}" does not exist.')
        
        attrs['service'] = service
        return attrs