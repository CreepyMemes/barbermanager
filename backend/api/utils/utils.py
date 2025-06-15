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
    Admin,
    Appointment,
    Availability,
    Service,
    Review,
    AppointmentStatus,
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


def send_client_reminder_email(client, barber, appointment_datetime):
    """
    Sends a reminder email to the client 1 hour before their appointment.
    """
    subject = '[BarberManager] Appointment Reminder'
    message = (
        f'Hi {client},\n\n'
        f'This is a reminder for your upcoming appointment with the barber {barber} '
        f'on {appointment_datetime.strftime("%Y-%m-%d at %H:%M")}.\n\n'
        'Please arrive on time.\n'
        'Thank you for using BarberManager!'
    )
    send_mail(subject, message, 'barber.manager.verify@gmail.com', [client.email])


def send_barber_reminder_email(barber, client, appointment_datetime):
    """
    Sends a reminder email to the barber 1 hour before an appointment.
    """
    subject = '[BarberManager] Upcoming Appointment Reminder'
    message = (
        f'Dear {barber},\n\n'
        f'This is a reminder that you have an appointment with the client {client} '
        f'on {appointment_datetime.strftime("%Y-%m-%d at %H:%M")}.\n\n'
        'Get ready to provide great service!\n'
        'BarberManager Team'
    )
    send_mail(subject, message, 'barber.manager.verify@gmail.com', [barber.email])

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
    

class AdminValidationMixin:
    """
    Mixin to validate that a admin_id from context exists and is active. Also adds 'admin' to attrs.
    """
    def validate_admin(self, attrs):
        admin_id = self.context.get('admin_id')

        try:
            admin = Admin.objects.get(pk=admin_id, is_active=True)
        except Admin.DoesNotExist:
            raise serializers.ValidationError(f'Admin with ID: "{admin_id}" does not exist or is inactive.')
        
        attrs['admin'] = admin
        return attrs
    

class AppointmentValidationMixin:
    """
    Mixin that rovides validation methods for appointment management:

    - Ensures that a client and barber do not have conflicting appointments on the same date or time slot, and that a client cannot have multiple ongoing appointments.
    - Verifies provided services all belong to the specified barber before creating or modifying an appointment.
    - Checks that an availability entry exists for the barber on the desired date, and that the requested time slot is included in the barber's available slots.
    - Confirms the existence of a specific appointment for the client and ensures it is ONGOING before allowing cancellation.
    """
    def validate_services_belong_to_barber(self, attrs):
        barber = attrs['barber']
        services = attrs['services']

        for service in services:
            if service.barber_id != barber.id:
                raise serializers.ValidationError(f'Service with ID "{service.id}" for the barber "{barber}" does not exist.')
            
        return attrs

    def validate_appointment_date_and_slot(self, attrs):
        client = attrs['client']
        barber = attrs['barber']
        appointment_date = attrs['date']
        appointment_slot = attrs['slot']

        if Appointment.objects.filter(client=client, status=AppointmentStatus.ONGOING.value).exists():
            raise serializers.ValidationError(f'Client: "{client}" already has an ONGOING appointment.')

        if Appointment.objects.filter(client=client, date=appointment_date).exclude(status=AppointmentStatus.CANCELLED.value).exists():
            raise serializers.ValidationError(f'Appointment for the date "{appointment_date}" for the client: "{client}" already exists.')

        if Appointment.objects.filter(barber=barber, date=appointment_date, slot=appointment_slot).exclude(status=AppointmentStatus.CANCELLED.value).exists():
            raise serializers.ValidationError(f'Appointment for the date: "{appointment_date}" in the slot: "{appointment_slot}" for the barber: "{barber}" already exists.')

        try:
            availability = Availability.objects.get(barber=barber, date=appointment_date)
        except Availability.DoesNotExist:
            raise serializers.ValidationError(f'Barber is not available on "{appointment_date}".')
        
        slot_str = appointment_slot.strftime('%H:%M')

        if slot_str not in availability.slots:
            raise serializers.ValidationError(f'Barber: "{barber}" is not available at "{slot_str}" on "{appointment_date}".')

        return attrs
    
    def validate_find_appointment(self, attrs):
        client = attrs['client']
        appointment_id = self.context.get('appointment_id')

        try:
            appointment = Appointment.objects.get(pk=appointment_id, client=client)
        except Appointment.DoesNotExist:
            raise serializers.ValidationError(f'Appointment with ID "{appointment_id}" for the client: "{client}" does not exist.')
        
        if appointment.status != AppointmentStatus.ONGOING.value:
            raise serializers.ValidationError('Only ONGOING appointments can be cancelled.')

        attrs['appointment'] = appointment
        return attrs


class AvailabilityValidationMixin:
    """
    Mixin that provides validation methods for availability management:

    - Ensures a barber does not already have an availability set for the same date, preventing duplicate availabilities on a single day.
    - Validates the existence of an availability entry for the given barber and specified ID before allowing retrieval or update operations.
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
    Mixin that provides validation methods for service-related operations:

    - Ensures a barber does not already have a service with the same name (case-insensitive) before creating or updating a service.
    - Ensures a service with the given ID exists and is owned by the specified barber before proceeding with actions that need to fetch or validate a particular service.
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

    def validate_find_service(self, attrs):
        barber = attrs['barber']
        service_id = self.context.get('service_id')

        try:
            service = Service.objects.get(barber=barber, pk=service_id)
        except Service.DoesNotExist:
            raise serializers.ValidationError(f'Service with the ID: "{service_id}" for the barber: "{barber}" does not exist.')
        
        attrs['service'] = service
        return attrs
    

class ReviewValidationMixin:
    """
    Mixin that provides validation methods for review-related actions:
    
    - Ensures an appointment exists, belongs to the client, is completed, and has not yet been reviewed by the client for the barber before allowing review creation.
    - Ensures a review exists and belongs to the requesting client when retrieving or modifying a review.
    """
    def validate_appointment_for_review(self, attrs):
        client = attrs['client']
        appointment_id = self.context.get('appointment_id')

        try:
            appointment = Appointment.objects.get(pk=appointment_id, client=client)
        except Appointment.DoesNotExist:
            raise serializers.ValidationError(f'Appointment with ID: "{appointment_id}" for the client: "{client}" does not exist.')

        if appointment.status != AppointmentStatus.COMPLETED.value:
            raise serializers.ValidationError('Only COMPLETED appointments can be reviewed.')

        barber = appointment.barber

        if Review.objects.filter(client=client, barber=barber).exists():
            raise serializers.ValidationError(f'Client: "{client}" review for the barber: "{barber}" already exists.')
        
        attrs['appointment'] = appointment
        attrs['barber'] = barber
        return attrs
    
    def validate_find_review(self, attrs):
        client = attrs['client']
        review_id = self.context.get('review_id')

        try:
            review = Review.objects.get(client=client, pk=review_id)
        except Review.DoesNotExist:
            raise serializers.ValidationError(f'Review with the ID: "{review_id}" for the client: "{client}" does not exist.')
        
        attrs['review'] = review
        return attrs
    


class GetBarbersMixin:
    """
    Mixin that provides getter methods to list all barbers for public use or admins.
    """
    def get_barbers_public(self):
        barbers = Barber.objects.filter(is_active=True)
        return [{
            'id': b.id, 
            'username': b.username, 
            'name': b.name,
            'surname': b.surname,
            'description': b.description
        } for b in barbers]
    
    def get_barbers_admin(self):
        barbers = Barber.objects.filter()
        return [{
            'id': b.id, 
            'is_active': b.is_active,
            'username': b.username, 
            'email': b.email, 
            'name': b.name,
            'surname': b.surname,
            'description': b.description
        } for b in barbers]


class GetAppointmentsMixin:
    """
    Mixin that provides getter methods for appointments for clients, barbers or admins.
    """
    def get_appointments_client(self, client_id):
        appointments = Appointment.objects.filter(client_id=client_id)
        return [{
            'id': a.id, 
            'barber_id': a.barber.id,
            'date': a.date, 
            'slot': a.slot.strftime("%H:%M"), 
            'services': [s.id for s in a.services.all()], 
            'status': a.status,
            'reminder_email_sent': a.reminder_email_sent,
        } for a in appointments]
    
    def get_appointments_barber(self, barber_id):
        appointments = Appointment.objects.filter(barber_id=barber_id, status=AppointmentStatus.ONGOING.value)
        return [{
            'id': a.id, 
            'client_full_name': f'{a.client.name} {a.client.surname}', 
            'date': a.date, 
            'slot': a.slot.strftime("%H:%M"), 
            'services': [s.id for s in a.services.all()], 
            'status': a.status,
            'reminder_email_sent': a.reminder_email_sent,
        } for a in appointments]
    
    def get_appointments_admin(self):
        appointments = Appointment.objects.all()
        return [{
            'id': a.id, 
            'client_id': a.client.id, 
            'barber_id': a.barber.id, 
            'date': a.date, 
            'slot': a.slot.strftime("%H:%M"), 
            'services': [s.id for s in a.services.all()], 
            'status': a.status,
            'reminder_email_sent': a.reminder_email_sent,
        } for a in appointments]
    

class GetReviewsMixin:
    """
    Mixin that provides getter methods for reviews for clients or barbers.
    """
    def get_reviews_client(self, client_id):
        reviews = Review.objects.filter(client_id=client_id).select_related('barber', 'appointment')
        return [{
            'id': r.id,
            'appointment_id': r.appointment.id,
            'barber_id': r.barber.id,
            'rating': r.rating,
            'comment': r.comment,
            'created_at': r.created_at.strftime('%Y-%m-%d'),
            'edited_at': r.edited_at.strftime('%Y-%m-%d') if r.edited_at else None
        } for r in reviews]
    
    def get_reviews_barber(self, barber_id):
        reviews = Review.objects.filter(barber_id=barber_id).select_related('client', 'appointment')
        return [{
            'id': r.id,
            'appointment_id': r.appointment.id,
            'client_full_name': f'{r.client.name} {r.client.surname}', 
            'rating': r.rating,
            'comment': r.comment,
            'created_at': r.created_at.strftime('%Y-%m-%d'),
            'edited_at': r.edited_at.strftime('%Y-%m-%d') if r.edited_at else None
        } for r in reviews]
    
    def get_reviews_admin(self):
        reviews = Review.objects.all().select_related('client', 'barber', 'appointment')
        return [{
            'id': r.id, 
            'appointment_id': r.appointment.id,
            'client_id': r.client.id, 
            'barber_id': r.barber.id, 
            'rating': r.rating,
            'comment': r.comment,
            'created_at': r.created_at.strftime('%Y-%m-%d'),
            'edited_at': r.edited_at.strftime('%Y-%m-%d') if r.edited_at else None
        } for r in reviews]


class GetServicesMixin:
    """
    Mixin that provides getter methods for services for barbers.
    """
    def get_services_barber(self, barber_id):
        services = Service.objects.filter(barber_id=barber_id)
        return [{
            'id': s.id,
            'name': s.name, 
            'price': s.price
        } for s in services]
    

class GetAvailabilitiesMixin:
    """
    Mixin that provides getter methods for services for barbers.
    """
    def get_availabilities_barber(self, barber_id):
        availabilities = Availability.objects.filter(barber_id=barber_id)
        return [{
            'id': a.id, 
            'date': a.date, 
            'slots': a.slots
        } for a in availabilities]
