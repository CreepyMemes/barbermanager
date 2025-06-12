import logging
from django.utils import timezone
from django.db.models import Q
from celery import shared_task
from .models import (
    Appointment, 
    AppointmentStatus,
)


logger = logging.getLogger(__name__)


@shared_task
def complete_ongoing_appointments():
    """
    Background task that automaically marks ONGOING appointments to COMPLETE when they are due.
    """
    logger.warning("Running 'complete_past_appointments' via CELERY BEAT")

    date_today = timezone.now().date()
    time_now = timezone.now().time()

    # Only mark ONGOING as COMPLETE if (date < date_today) OR if (date == date_today AND slot <= time_now)
    appointments = Appointment.objects.filter(status=AppointmentStatus.ONGOING.value).filter(
        (Q(date__lt=date_today) | Q(date=date_today, slot__lte=time_now))
    )

    return appointments.update(status=AppointmentStatus.COMPLETED.value)