from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from celery import shared_task
from .models import (
    Appointment, 
    AppointmentStatus,
)
from .utils import(
    send_client_reminder_email,
    send_barber_reminder_email,
)


@shared_task
def complete_ongoing_appointments():
    """
    Background task that automaically marks ONGOING appointments to COMPLETE when they are due.
    """
    now = timezone.localtime(timezone.now())  # Italy time!
    
    date_today = now.date()
    time_now = now.time()

    # Only mark ONGOING as COMPLETE if (date < date_today) OR if (date == date_today AND slot <= time_now)
    appointments = Appointment.objects.filter(status=AppointmentStatus.ONGOING.value).filter((Q(date__lt=date_today) | Q(date=date_today, slot__lte=time_now)))

    return appointments.update(status=AppointmentStatus.COMPLETED.value)


@shared_task
def send_appointment_reminders():
    """
    Background task that automaically sends reminder emails for appointments 1 hour before they are due.
    """
    now = timezone.localtime(timezone.now())  # Italy time!

    date_today = now.date()
    time_hour_later = now + timedelta(hours=1)

    # Only get appointments with ONGOING and COMPLETED status, for today, for which reminder not sent, whose datetime is within the next hour
    statuses = [AppointmentStatus.ONGOING.value, AppointmentStatus.COMPLETED.value]
    appointments = Appointment.objects.filter(status__in=statuses, reminder_email_sent=False, date=date_today)

    for appointment in appointments:
        appointment_date = timezone.make_aware(datetime.combine(appointment.date, appointment.slot), timezone.get_current_timezone())
        
        if (now - timedelta(minutes=10)) < appointment_date <= time_hour_later:
            send_client_reminder_email(appointment.client, appointment.barber, appointment_date)
            send_barber_reminder_email(appointment.barber, appointment.client, appointment_date)
            
            appointment.reminder_email_sent = True
            appointment.save(update_fields=['reminder_email_sent'])