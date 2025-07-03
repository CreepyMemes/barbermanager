from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import Q, UniqueConstraint, Avg, Sum
from django.db import models
from enum import Enum

class Roles(Enum):
    """
    User role definitions: Admin, Client, Barber.
    """
    ADMIN = 'ADMIN'
    CLIENT = 'CLIENT'
    BARBER = 'BARBER'

    @classmethod
    def choices(cls):
        return [(role.value, role.name) for role in cls]
    

class UserManager(BaseUserManager):
    """
    Custom user manager to handle user and superuser creation.
    """
    def create_user(self, username, email=None, password=None, **extra_fields):
        
        if not username:
            raise ValueError('Username is required')
        
        role = extra_fields.get('role', Roles.CLIENT.value)

        if role != Roles.ADMIN.value and not email:
            raise ValueError('Email is required for non-admin users')

        if email:
            email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', Roles.ADMIN.value)

        if not username:
            raise ValueError('Superuser must have a username')
        
        if extra_fields.get('role') != Roles.ADMIN.value:
            raise ValueError('Superuser must have role=ADMIN')
        
        admin = Admin(username=username, **extra_fields)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin


class User(AbstractUser):
    """
    Custom user model using our custom manager.
    """
    def _get_profile_image_path(instance, filename):
        """
        Methohd that imports here to avoid circular import issues.
        """
        from ..utils import get_profile_image_path
        return get_profile_image_path(instance, filename)
    
    def _username_validator():
        """
        Methohd that imports here to avoid circular import issues.
        """
        from ..utils import username_validator
        return username_validator
    
    username = models.CharField(validators=[_username_validator()], max_length=150, unique=True)
    email = models.EmailField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=Roles.choices(), default=Roles.CLIENT.value)
    profile_image = models.ImageField(upload_to=_get_profile_image_path, null=True, blank=True)
    

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['email'],
                condition=~Q(role=Roles.ADMIN.value),  # only enforce uniqueness for non-admins
                name='unique_email_non_admin'
            )
        ]
    
    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'is_active': self.is_active,
            'username': self.username,
            'email': self.email,
            'profile_image': self.profile_image.url if self.profile_image else None,
        }


class Admin(User):
    """
    Admins are created by the system using the `createsuperuser` command.
    They are granted full permissions (staff and superuser) and do not require an email.
    """
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = Roles.ADMIN.value

        self.is_staff = True
        self.is_superuser = True

        super().save(*args, **kwargs)

    @property
    def total_clients(self):
        """
        Returns the sum of all the registered clients in the platform
        """
        from .user import Client
        return Client.objects.filter(is_active=True).count()
    
    @property
    def total_barbers(self):
        """
        Returns the sum of all the registered barbers in the platform
        """
        from .user import Barber
        return Barber.objects.filter(is_active=True).count()
    
    @property
    def total_appointments(self):
        """
        Returns the sum of all the booked appointments in the platform
        """
        from .appointment import Appointment
        return Appointment.objects.count()

    @property
    def completed_appointments(self):
        """
        Returns the sum of all the completed appointments in the platform
        """
        from .appointment import Appointment, AppointmentStatus
        return Appointment.objects.filter(status=AppointmentStatus.COMPLETED.value).count()
    
    @property
    def cancelled_appointments(self):
        """
        Returns the sum of all the cancelled appointments in the platform
        """
        from .appointment import Appointment, AppointmentStatus
        return Appointment.objects.filter(status=AppointmentStatus.CANCELLED.value).count()
    
    @property
    def ongoing_appointments(self):
        """
        Returns the sum of all the ongoing appointments in the platform
        """
        from .appointment import Appointment, AppointmentStatus
        return Appointment.objects.filter(status=AppointmentStatus.ONGOING.value).count()
    
    @property
    def total_revenue(self):
        """
        Returns the sum of the services in all completed appointments, for total platform revenue
        """
        from .appointment import Appointment, AppointmentStatus
        revenue = (
            Appointment.objects.filter(status=AppointmentStatus.COMPLETED.value)
            .annotate(price_sum=Sum('services__price'))
            .aggregate(total=Sum('price_sum'))['total']
        )
        return float(revenue) if revenue else 0.0

    @property
    def total_reviews(self):
        """
        Returns the sum of all reviews posted in the platform
        """
        from .appointment import Review
        return Review.objects.count()
    
    @property
    def average_rating(self):
        """
        Returns the average rating of all reviewes posted in the platrofm
        """
        from .appointment import Review
        avg = Review.objects.aggregate(avg=Avg('rating'))['avg']
        return round(float(avg), 2) if avg else 0.0
    
    def to_dict(self):
        base = super().to_dict()
        base.update({
            'total_clients': self.total_clients,
            'total_barbers': self.total_barbers,
            'total_appointments': self.total_appointments,
            'completed_appointments': self.completed_appointments,
            'cancelled_appointments': self.cancelled_appointments,
            'ongoing_appointments': self.ongoing_appointments,
            'total_revenue': self.total_revenue,
            'total_reviews': self.total_reviews,
            'average_rating': self.average_rating,
        })
        return base


class Client(User):
    """
    Clients are regular users who can register themselves via the API.
    They must provide a valid email and username during registration.
    """
    def _phone_number_validator():
        """
        Methohd that imports here to avoid circular import issues.
        """
        from ..utils import phone_number_validator
        return phone_number_validator
    
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone_number = models.CharField(validators=[_phone_number_validator()], max_length=16, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = Roles.CLIENT.value

        if not self.email:
            raise ValueError('Client must have an email')
        
        super().save(*args, **kwargs)

    @property
    def appointments(self):
        """
        Returns a list of dicts representing all this client's appointments.
        """
        return [appointment.to_dict() for appointment in self.appointments_created.all()]

    @property
    def completed_appointments(self):
        """
        Returns the sum of all the completed appointments for this cllient.
        """
        from .appointment import AppointmentStatus
        return self.appointments_created.filter(status=AppointmentStatus.COMPLETED.value).count()
    

    @property
    def next_appointment(self):
        """
        Returns the single ongoing Appointment instance for this client, or None.
        """
        from .appointment import AppointmentStatus
        return self.appointments_created.filter(status=AppointmentStatus.ONGOING.value).first().to_dict()

    @property
    def reviews(self):
        """
        Returns a list of dicts representing all reviews made by this client.
        """
        return [review.to_dict() for review in self.client_reviews.all()]
    
    def to_dict(self):
        base = super().to_dict()
        base.update({      
            'name': self.name,
            'surname': self.surname,
            'phone_number': self.phone_number,
            'appointments': self.appointments,
            'completed_appointments': self.completed_appointments,
            'next_appointment': self.next_appointment,
            'reviews': self.reviews,
        })
        return base


class Barber(User):
    """
    Barbers can only register if invited by an admin. They register by 
    providing a username and password, email is set by admin invitation.
    """
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = Roles.BARBER.value

        if not self.email:
            raise ValueError('Barber must have an email')
        
        super().save(*args, **kwargs)
    
    @property
    def services(self):
        """
        Returns a list of dicts representing this barber's services.
        """
        return [service.to_dict() for service in self.services_offered.all()]
    
    @property
    def availabilities(self):
        """
        Returns a list of dicts representing this barber's availabilities.
        """
        return [availability.to_dict() for availability in self.availabilities_assigned.all()]
    
    @property
    def completed_appointments(self):
        """
        Returns the sum of all the completed appointments for this barber.
        """
        from .appointment import AppointmentStatus
        return self.appointments_received.filter(status=AppointmentStatus.COMPLETED.value).count()
    
    @property
    def ongoing_appointments(self):
        """
        Returns a list of all the ongoing appointments for this barber.
        """
        from .appointment import AppointmentStatus
        return [appointment.to_dict() for appointment in self.appointments_received.filter(status=AppointmentStatus.ONGOING.value)]

    @property
    def total_revenue(self):
        from .appointment import AppointmentStatus
        """
        Returns the sum of the services in all completed appointments for this barber.
        """
        revenue = (
            self.appointments_received.filter(status=AppointmentStatus.COMPLETED.value)
            .annotate(price_sum=Sum('services__price'))
            .aggregate(total=Sum('price_sum'))['total']
        )
        return float(revenue) if revenue else 0.0
    
    @property
    def reviews(self):
        """
        Returns a list of dicts representing this barber's reviews.
        """
        return [review.to_dict() for review in self.barber_reviews.all()]
    
    @property
    def average_rating(self):
        """
        Returns the average rating of this barber, or None if no reviews exist.
        """
        avg = self.barber_reviews.aggregate(avg=Avg('rating'))['avg']
        return round(float(avg), 2) if avg else 0.0
    
    def to_dict(self):
        """
        Returns a JSON-serializable dict representation of the review.
        """
        base = super().to_dict()
        base.update({
            'name': self.name,
            'surname': self.surname,
            'description': self.description,
            'services': self.services,
            'availabilities': self.availabilities,
            'ongoing_appointments': self.ongoing_appointments,
            'completed_appointments': self.completed_appointments,
            'total_revenue': self.total_revenue,
            'reviews': self.reviews,
            'average_rating': self.average_rating,
        })
        return base