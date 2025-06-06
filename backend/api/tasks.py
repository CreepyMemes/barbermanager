from django.utils import timezone
from celery import shared_task
from .models import (
    Appointment, 
    AppointmentStatus,
)

@shared_task
def complete_past_appointments():
    now = timezone.now().date()
    time_now = timezone.now().time()
    # Only mark as complete if appointment date < now (all past days)
    # Or if today and slot < now
    appointments = Appointment.objects.filter(
        status=AppointmentStatus.ONGOING.value
    ).filter(
        # Either it's a previous day, or it's today and time has passed
        (Q(date__lt=now) | Q(date=now, slot__lt=time_now))
    )

    for appointment in appointments:
        appointment.status = AppointmentStatus.COMPLETED.value
        appointment.save()