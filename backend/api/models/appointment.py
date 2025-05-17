from django.db import models
from enum import Enum
from .user import Roles, User


class AppointmentStatus(Enum):
    """
    Enumeration of possible statuses for an appointment.
    """
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    @classmethod
    def choices(cls):
        return [(status.value, status.name) for status in cls]
    

class Service(models.Model):
    """
    A service offered by a barber.
    Each service is associated with exactly one barber.
    Barbers can offer multiple different services.
    """
    barber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': Roles.BARBER.value},
        related_name='services'
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.barber.email}"
    
    
class Availability(models.Model):
    """
    Represents a one-hour time slot of availability for a barber.
    Managed by admins only.
    """
    barber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role':Roles.BARBER.value},
        related_name='availabilities',
    )
    date=models.DateField()
    hour = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ['barber', 'date', 'hour']

    def __str__(self):
        return f'{self.barber.email} - {self.date} {self.hour}'


class Appointment(models.Model):
    """
    Represents a booked appointment made by a client with a barber.
    Clients can select one barber and choose one or more services offered by that barber,
    scheduled for a specific availability slot.
    """
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': Roles.CLIENT.value},
        related_name='appointments',
    )
    barber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': Roles.BARBER.value},
        related_name='appointments_received'
    )
    status = models.CharField(
        max_length=10,
        choices=AppointmentStatus.choices(),
        default=AppointmentStatus.ONGOING.value
    )
    services = models.ManyToManyField(Service)
    availability = models.OneToOneField(Availability, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.email} -> {self.barber.email} on {self.availability.date}"
    

class Review(models.Model):
    """
    A review submitted by a client for a barber, linked to a completed appointment.
    """
    appointment = models.OneToOneField(
        Appointment, 
        on_delete=models.CASCADE, 
        related_name='appointment_review'
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': Roles.CLIENT.value},
        related_name='client_reviews'
    )
    barber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': Roles.BARBER.value},
        related_name='barber_reviews'
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['client', 'barber']

    def __str__(self):
        return f"Review by {self.client.email} for {self.barber.email} - {self.rating} stars"