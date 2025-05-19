from django.db import models
from enum import Enum
from .user import Barber, Client

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
    Represents a service offered by a barber.
    Each service is tied to one barber.
    Barbers can offer multiple services.
    """
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.barber.email}"


class Availability(models.Model):
    """
    Represents the availability of a barber for a given date.
    Contains a list of 1-hour slots as strings (e.g. "09:00", "10:00").
    Managed by admins only.
    """
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='availabilities',)
    date = models.DateField()
    slots = models.JSONField()  # Example: ["09:00", "10:00", "11:00"]
    
    class Meta:
        unique_together = ['barber', 'date']

    def __str__(self):
        return f'{self.barber.email} - {self.date} Slots: {self.slots}'


class Appointment(models.Model):
    """
    Represents a booked appointment made by a client with a barber.
    Clients can select one barber and choose one or more services offered by that barber 
    and one slot from the barber's availability.
    """
    client = models.ForeignKey( Client, on_delete=models.CASCADE, related_name='appointments',)
    barber = models.ForeignKey( Barber, on_delete=models.CASCADE, related_name='appointments_received')
    date = models.DateField()
    slot = models.TimeField()
    services = models.ManyToManyField(Service)
    status = models.CharField( max_length=10, choices=AppointmentStatus.choices(), default=AppointmentStatus.ONGOING.value)

    class Meta:
        unique_together = ['barber', 'date', 'slot']  # Prevent double booking on same slot

    def __str__(self):
        return f"{self.client.email} -> {self.barber.email} on {self.date} at {self.slot}"


class Review(models.Model):
    """
    Represents a client's single review for a barber after a completed appointment with them.
    """
    appointment = models.OneToOneField( Appointment,  on_delete=models.CASCADE,  related_name='appointment_review')
    client = models.ForeignKey( Client, on_delete=models.CASCADE, related_name='client_reviews')
    barber = models.ForeignKey( Barber, on_delete=models.CASCADE, related_name='barber_reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['client', 'barber']

    def __str__(self):
        return f"Review by {self.client.email} for {self.barber.email} - {self.rating} stars"
    