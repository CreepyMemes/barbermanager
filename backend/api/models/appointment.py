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
    Represents a specific service that a barber offers to clients.

    - Each service is linked to a single barber.
    - A barber can offer multiple different services, but cannot have two services with the same name.
    - Includes details such as the service name and its price.
    """
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['barber', 'name'], name='unique_service_name_per_barber')
        ]

    def __str__(self):
        return f"{self.name} - {self.barber.email}"


class Availability(models.Model):
    """
    Stores a barber's available time slots for client bookings on a particular date.

    - Each availability record is linked to one barber and one date.
    - The 'slots' field contains a list of available 1-hour time slots in "HH:MM" format.
    - Used by admins to manage and update barbers' availability for appointments.
    """
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='availabilities',)
    date = models.DateField()
    slots = models.JSONField()  # Example: ["09:00", "10:00", "11:00"]
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['barber', 'date'], name='unique_availability_date_per_barber')
        ]

    def __str__(self):
        return f'{self.barber.email} - {self.date} Slots: {self.slots}'


class Appointment(models.Model):
    """
    Represents a scheduled appointment booked by a client with a barber.

    - Each appointment records which client is booking, which barber, the date and time slot, and the selected services.
    - Clients may book only one appointment per date.
    - Prevents double-booking by ensuring a barber can have only one appointment per slot on a given date.
    - Tracks the appointment status (e.g., ongoing, completed, canceled).
    """
    client = models.ForeignKey( Client, on_delete=models.CASCADE, related_name='appointments',)
    barber = models.ForeignKey( Barber, on_delete=models.CASCADE, related_name='appointments_received')
    date = models.DateField()
    slot = models.TimeField()
    services = models.ManyToManyField(Service)
    status = models.CharField( max_length=10, choices=AppointmentStatus.choices(), default=AppointmentStatus.ONGOING.value)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['barber', 'date', 'slot'], name='unique_appointment_per_barber_date_slot'),
            models.UniqueConstraint(fields=['client', 'date'], name='unique_appointment_per_client_date'),
        ]

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
    