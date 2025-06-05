from django.urls import reverse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import  force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from ..models import (
    User, 
    Barber,
    Availability,
    Service
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
            raise serializers.ValidationError("A user with this email already exists.")
        return email


class UsernameValidationMixin:
    """
    Utility mixin to handle common username validation checks
    """
    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username is already taken.")
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
    

class BarberValidationMixin:
    """
    Mixin to validate that a barber_id from context exists and is active. Also adds 'barber' to attrs.
    """
    def validate_barber(self, attrs):
        barber_id = self.context.get('barber_id')

        try:
            barber = Barber.objects.get(pk=barber_id, is_active=True)
        except Barber.DoesNotExist:
            raise serializers.ValidationError('Barber with this ID does not exist or is inactive.')
        
        attrs['barber'] = barber
        return attrs


class NewAvailabilityValidationMixin:
    """
    Mixin to validate if the given date for the specific barber doesn't already have existing availability
    """
    def validate_new_date(self, attrs):
        barber = attrs['barber']
        date = attrs['date']

        if Availability.objects.filter(barber=barber, date=date).exists():
            raise serializers.ValidationError(f'Availability for the date: {date} already exists.')
        
        return attrs


class FindAvailabilityValidationMixin:
    """
    Mixin to validate if the given date for the specific barber has an existing availabililty
    """
    def validate_find_date(self, attrs):
        barber = attrs['barber']
        date = attrs['date']

        try:
            availability = Availability.objects.get(barber=barber, date=date)
        except Availability.DoesNotExist:
            raise serializers.ValidationError(f'No availability exists for the date: {date}.')
        
        attrs['availability'] = availability
        return attrs
    
class ServiceValidationMixin:
    """
    Mixin to validate that a service_id from context exists and is active. Also adds 'service' to attrs.
    """
    def validate_service(self, attrs):
        service_id = self.context.get('service_id')

        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            raise serializers.ValidationError('Service with this ID does not exist or is inactive.')
        
        attrs['service'] = service
        return attrs
