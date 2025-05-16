from django.db import models
from enum import Enum
from .user import Roles, User


class AppointmentStatus(Enum):
    """
    Enumeration of possible statuses for an appointment.
    
    Statuses include:
    - ONGOING: Appointment is currently scheduled or in progress.
    - COMPLETED: Appointment has been completed.
    - CANCELLED: Appointment has been cancelled.
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

    Fields:
    - barber: The barber offering this service.
    - name: Name of the service.
    - price: Price of the service, with up to 6 digits total and 2 decimal places.
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

    Fields:
    - barber: The barber who is available during this slot.
    - date: The calendar date of the availability.
    - hour: The start time of the one-hour availability slot.
    - is_booked: Whether this slot has been booked by a client.
    
    Constraints:
    - Each barber can only have one availability entry per date and hour.
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

    Fields:
    - client: The client who booked the appointment.
    - barber: The barber with whom the appointment is booked.
    - status: Current status of the appointment (ongoing, completed, cancelled).
    - services: One or more services selected for the appointment.
    - availability: The specific availability slot booked.
    - created_at: Timestamp when the appointment was created.
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

    Fields:
    - appointment: The completed appointment this review is associated with (one-to-one).
    - client: The client who submitted the review (must have CLIENT role).
    - barber: The barber being reviewed (must have BARBER role).
    - rating: Numerical rating given by the client (e.g., 1 to 5).
    - comment: Optional text comment provided by the client.
    - created_at: Timestamp when the review was created.
    
    Constraints:
    - One review per appointment (enforced by OneToOneField).
    - One review per client-barber pair (enforced by unique_together).
    - Only clients can create reviews.
    - Reviews can only be made for barbers associated with completed appointments.
    """
    appointment = models.OneToOneField(
        Appointment, 
        on_delete=models.CASCADE, 
        related_name='review'
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': Roles.CLIENT.value},
        related_name='reviews'
    )
    barber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': Roles.BARBER.value},
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['client', 'barber']

    def __str__(self):
        return f"Review by {self.client.email} for {self.barber.email} - {self.rating} stars"