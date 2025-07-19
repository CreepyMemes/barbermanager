from django.db import models
from django.db.models import Q, Sum
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
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='services_offered')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['barber', 'name'], name='unique_service_name_per_barber')
        ]

    def to_dict(self):
        """
        Returns a JSON-serializable dict representation of the service.
        """
        return {
            'id': self.id,
            'barber_id': self.barber.id,
            'name': self.name,
            'price': float(self.price),
        }
    

class Appointment(models.Model):
    """
    Represents a scheduled appointment booked by a client with a barber.

    - Each appointment records which client is booking, which barber, the date and time slot, and the selected services.
    - Clients may book only one appointment per date.
    - Prevents double-booking by ensuring a barber can have only one appointment per slot on a given date.
    - Tracks the appointment status (e.g., ongoing, completed, canceled).
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments_created')
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='appointments_received')
    date = models.DateField()
    slot = models.TimeField()
    services = models.ManyToManyField(Service, through='AppointmentService', related_name='appointments')
    status = models.CharField( max_length=10, choices=AppointmentStatus.choices(), default=AppointmentStatus.ONGOING.value)
    reminder_email_sent = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client', 'date'], condition=~Q(status=AppointmentStatus.CANCELLED.value), name='unique_appointment_per_client_date_if_not_cancelled'),
            models.UniqueConstraint(fields=['barber', 'date', 'slot'], condition=~Q(status=AppointmentStatus.CANCELLED.value), name='unique_appointment_per_barber_date_slot_if_not_cancelled'),
        ]

    @property
    def service_ids(self):
        """
        Returns a list of dicts representing this barber's services.
        """
        return list(self.services.values_list('id', flat=True))
    
    @property
    def services_list(self):
        """
        Returns a list of dicts of all services associated with this appointment at booking time.
        """
        return [service.to_dict() for service in self.line_items.all()]
    
    @property
    def amount_spent(self):
        """
        Returns the total price of all services in this appointment.
        """
        total = self.line_items.aggregate(total=Sum('price'))['total']
        return float(total) if total else 0.0
    
    def to_dict(self):
        """
        Returns a JSON-serializable dict representation of the appointment.
        """
        return {
            'id': self.id,
            'barber_id': self.barber.id,
            'client_id': self.client.id,
            'amount_spent': self.amount_spent,
            'services': self.services_list,
            'date': self.date,
            'slot': self.slot.strftime("%H:%M"),
            'status': self.status,
            'reminder_email_sent': self.reminder_email_sent,
        }


class AppointmentService(models.Model):
    """
    Stores a copy ("line item") of each service included in an appointment, capturing its details at the time of booking.

    - Links to a specific appointment via a foreign key.
    - Snapshots the service name and price at booking time, so appointment history is preserved even if the Service is changed or deleted.
    - Optionally links back to the original Service for reference, but original_service may be null if the Service is removed from the system.
    """
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, related_name='line_items')
    original_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def to_dict(self):
        return {
            'id': self.id,
            'original_service_id': self.original_service_id,
            'name': self.name,
            'price': float(self.price),
        }

class Availability(models.Model):
    """
    Stores a barber's available time slots for client bookings on a particular date.

    - Each availability record is linked to one barber and one date.
    - The 'slots' field contains a list of available 1-hour time slots in "HH:MM" format.
    - Used by admins to manage and update barbers' availability for appointments.
    """
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='availabilities_assigned',)
    date = models.DateField()
    slots = models.JSONField()  # Example: ["09:00", "10:00", "11:00"]
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['barber', 'date'], name='unique_availability_date_per_barber')
        ]

    def to_dict(self):
        """
        Returns a JSON-serializable dict representation of the availability.
        """
        return {
            'id': self.id,
            'barber_id': self.barber.id,
            'date': self.date,
            'slots': self.slots,
        }


class Review(models.Model):
    """
    Represents a single review by a client for a barber after a completed appointment.
    
    - Each review is linked to one appointment, one client, and one barber.
    - A client can only leave one review per barber, regardless of the number of appointments.
    - Only appointments that have been completed should be reviewed.
    - Includes rating, optional comment, and timestamp of creation.
    """
    appointment = models.OneToOneField(Appointment,  on_delete=models.CASCADE,  related_name='appointment_review')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_reviews')
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='barber_reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True) 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client', 'barber'], name='unique_client_review_per_barber')
        ]

    def to_dict(self):
        """
        Returns a JSON-serializable dict representation of the review.
        """
        return {
            'id': self.id,
            'appointment_id': self.appointment.id,
            'client_id': self.client.id,
            'barber_id': self.barber.id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'edited_at': self.edited_at.strftime('%Y-%m-%d') if self.edited_at else None,
        }