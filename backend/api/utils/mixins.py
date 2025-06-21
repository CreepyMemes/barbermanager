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
    def validate_email_unique(self, attrs, user_instance=None):
        email = attrs['email']

        user = User.objects.filter(email=email)

        if user_instance:
            user = user.exclude(pk=user_instance.pk)

        if user.exists():
            raise serializers.ValidationError(f'The email "{email}" is already taken.')
        
        attrs['email'] = email
        return attrs


class UsernameValidationMixin:
    """
    Utility mixin to handle common username validation checks
    """
    def validate_username_unique(self, attrs, user_instance=None): 
        username = attrs['username']

        user = User.objects.filter(username=username)

        if user_instance:
            user = user.exclude(pk=user_instance.pk)
        
        if user.exists():
            raise serializers.ValidationError(f'The username "{username}" is already taken.')
        
        attrs['username'] = username
        return attrs


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
    

class UserValidationMixin:
    """
    Mixin to validate that a user_id from context exists and is active. Also adds 'user' to attrs.
    """
    def validate_user(self, attrs):
        user_id = self.context.get('user_id')

        try:
            user = User.objects.get(pk=user_id, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError(f'User with ID: "{user_id}" does not exist or is inactive.')
        
        attrs['user'] = user
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


class GetAdminsMixin:
    """
    Mixin for retrieving and serializing Admin models.
    """
    def get_admins_queryset(self):
        """
        Returns Admin queryset in the system.
        """
        return Admin.objects.all()
    
    def get_admin_private(self, admin):
        """
        Returns all data for a single admin.
        """
        return admin.to_dict()
    
    def get_admins_private(self):
        """
        Returns all admins as full dicts.
        """
        return [self.get_admin_private(a) for a in self.get_admins_queryset()]
    

class GetBarbersMixin:
    """
    Mixin for retrieving and serializing Barber models.
    """
    _PUBLIC_EXCLUDES = ['email', 'username', 'availabilities', 'is_active']

    def get_barbers_queryset(self, show_all=False):
        """
        Returns Barber queryset in the system.
        If show_all is True, returns all barbers.
        """
        return Barber.objects.filter(is_active=True) if not show_all else Barber.objects.all()
    
    def get_barber_public(self, barber):
        """
        Returns only the public data for a single barber.
        """
        data = barber.to_dict().copy()
        for field in self._PUBLIC_EXCLUDES:
            data.pop(field, None)
        return data
    
    def get_barber_private(self, barber):
        """
        Returns all data for a single barber.
        """
        return barber.to_dict()
    
    def get_barbers_private(self, show_all=False):
        """
        Returns all barbers as full dicts (all or only active).
        """
        return [self.get_barber_private(b) for b in self.get_barbers_queryset(show_all=show_all)]
    
    def get_barbers_public(self):
        """
        Returns all active barbers as public dicts.
        """
        return [self.get_barber_public(b) for b in self.get_barbers_queryset()]


class GetClientsMixin:
    """
    Mixin for retrieving and serializing Client models.
    """
    _PUBLIC_EXCLUDES = ['email', 'name', 'surname', 'phone_number', 'appointments', 'is_active']

    def get_clients_queryset(self, show_all=False):
        """
        Returns Client queryset in the system.
        If show_all is True, returns all clients.
        """
        return Client.objects.filter(is_active=True) if not show_all else Client.objects.all()
    
    def get_client_public(self, client):
        """
        Returns only the public data for a single client.
        """
        data = client.to_dict().copy()
        for field in self._PUBLIC_EXCLUDES:
            data.pop(field, None)
        return data
    
    def get_client_private(self, client):
        """
        Returns all data for a single client.
        """
        return client.to_dict()
    
    def get_clients_private(self, show_all=False):
        """
        Returns all clients as full dicts (all or only active).
        """
        return [self.get_client_private(b) for b in self.get_clients_queryset(show_all=show_all)]
    
    def get_clients_public(self):
        """
        Returns all active clients as public dicts.
        """
        return [self.get_client_public(b) for b in self.get_clients_queryset()]
    

class GetAvailabilitiesMixin:
    """
    Mixin for retrieving and serializing Availability models.
    """
    def get_availabilities_queryset(self, barber_id, show_all=False):
        """
        Returns Availability queryset for a specific barber.
        If show_all is True, returns all availabilities.
        """
        return Availability.objects.filter(barber_id=barber_id) if not show_all else Availability.objects.all()
    
    def get_availability_public(self, availability):
        """
        Returns all data for a single availability.
        """
        return availability.to_dict()
    
    def get_availabilities_public(self, barber_id, show_all=False):
        """
        Returns all barbers as full dicts (all or only active).
        """
        return [self.get_availability_public(b) for b in self.get_availabilities_queryset(barber_id=barber_id, show_all=show_all)]


class GetServicesMixin:
    """
    Mixin for retrieving and serializing Service models.
    """
    def get_services_queryset(self, barber_id, show_all=False):
        """
        Returns Service queryset for a specific barber.
        If show_all is True, returns all services.
        """
        return Service.objects.filter(barber_id=barber_id) if not show_all else Service.objects.all()
    
    def get_service_public(self, service):
        """
        Returns all data for a single service.
        """
        return service.to_dict()
    
    def get_services_public(self, barber_id, show_all=False):
        """
        Returns all barbers as full dicts (all or only active).
        """
        return [self.get_service_public(b) for b in self.get_services_queryset(barber_id=barber_id, show_all=show_all)]


class GetAppointmentsMixin:
    """
    Mixin for retrieving and serializing Appointment models.
    """
    def get_appointments_queryset(self, barber_id=None, client_id=None, show_all=False):
        """
        Returns Appointment queryset filtered by barber or client.
        If show_all is True, returns all appointments.
        """
        if show_all:
            return Appointment.objects.all()
        
        if barber_id and client_id:
            raise serializers.ValidationError('Appointments Queryset Error: Provide only a barber_id or a client_id, not both.')

        if not barber_id and not client_id:
            raise serializers.ValidationError('Appointments Queryset Error: Provide either a barber_id or a client_id.')
        
        if barber_id:
            return Appointment.objects.filter(barber_id=barber_id)
        
        return Appointment.objects.filter(client_id=client_id)
    
    def get_appointment_public(self, appointment):
        """
        Returns all data for a single appointment.
        """
        return appointment.to_dict()
    

    def get_appointments_public(self, barber_id=None, client_id=None, show_all=False):
        """
        Returns all barbers as full dicts (all or only active).
        """
        return [self.get_appointment_public(b) for b in self.get_appointments_queryset(barber_id=barber_id, client_id=client_id, show_all=show_all)]
    

class GetReviewsMixin:
    """
    Mixin for retrieving and serializing Review models.
    """
    def get_reviews_queryset(self, barber_id=None, client_id=None, show_all=False):
        """
        Returns Review queryset filtered by barber or client.
        If show_all is True, returns all reviews.
        """
        if show_all:
            return Review.objects.all()
        
        if barber_id and client_id:
            raise serializers.ValidationError('Reviews Queryset Error: Provide only a barber_id or a client_id, not both.')

        if not barber_id and not client_id:
            raise serializers.ValidationError('Reviews Queryset Error: Provide either a barber_id or a client_id.')
        
        if barber_id:
            return Review.objects.filter(barber_id=barber_id)
        
        return Review.objects.filter(client_id=client_id)
    
    def get_review_public(self, review):
        """
        Returns all data for a single review.
        """
        return review.to_dict()
    
    def get_reviews_public(self, barber_id=None, client_id=None, show_all=False):
        """
        Returns all barbers as full dicts (all or only active).
        """
        return [self.get_review_public(b) for b in self.get_reviews_queryset(barber_id=barber_id, client_id=client_id, show_all=show_all)]