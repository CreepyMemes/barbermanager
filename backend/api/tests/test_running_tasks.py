import datetime
from unittest.mock import patch
from django.db.models import Q
from django.test import TestCase
from django.utils import timezone
from api.tasks import complete_ongoing_appointments, send_appointment_reminders
from api.models import (
    Barber,
    Client,
    Service,
    AppointmentService,
    Appointment,
    AppointmentStatus
)

@patch('django.core.mail.send_mail', return_value=1)
class RunningTasksTestCase(TestCase):
    """
    Unit tests for celery appointment tasks.
    """

    def setUp(self):
        # Create users
        self.barber = Barber.objects.create_user(
            username="bob",
            email="bob@example.com",
            password="pw",
            name="b",
            surname="b"
        )
        self.client = Client.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="pw",
            name="a",
            surname="a"
        )

        # Appointment parameters
        self.today = timezone.localdate()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.now = timezone.localtime(timezone.now()).replace(microsecond=0, second=0)
        self.now_time = self.now.time()
        self.past_time = (self.now - datetime.timedelta(hours=1)).time()
        self.future_time = (self.now + datetime.timedelta(hours=1)).time()

        # Service for appointments
        self.service = Service.objects.create(
            barber=self.barber,
            name="Shave",
            price=15
        )

    def _fresh_client(self, suffix):
        """
        Creates a fresh client per need.
        """
        return Client.objects.create_user(
            username=f"alice{suffix}",
            email=f"alice{suffix}@example.com",
            password="pw",
            name=f"a{suffix}",
            surname=f"a{suffix}"
        )

    def add_services(self, appointment, service_list):
        """
        Helper to bulk assign services via AppointmentService
        """
        for service in service_list:
            AppointmentService.objects.create(
                appointment=appointment,
                name=service.name,
                price=service.price,
                original_service=service
            )

    def create_appointment(self, *, date, slot, status=AppointmentStatus.ONGOING.value, reminder_email_sent=False, client=None):
        appointment = Appointment.objects.create(
            client=client if client is not None else self.client,
            barber=self.barber,
            date=date,
            slot=slot,
            status=status,
            reminder_email_sent=reminder_email_sent,
        )
        self.add_services(appointment, [self.service])
        return appointment

    @patch("api.tasks.timezone")
    def test_complete_ongoing_appointments_only_overdue(self, mocked_tz, mock_send_mail):
        """
        Only appointments whose (date < today) or (date == today and slot <= now)
        get marked COMPLETE if ONGOING.
        """
        fake_now = timezone.make_aware(datetime.datetime.combine(self.today, self.now_time))
        mocked_tz.now.return_value = fake_now
        mocked_tz.localtime.return_value = fake_now

        # Appointments for self.client (all unique date/client/barber/slot)
        appt_yest = self.create_appointment(date=self.yesterday, slot=self.past_time)  # should complete
        appt_today_past = self.create_appointment(date=self.today, slot=self.past_time)  # should complete

        # Use fresh clients & slots to avoid clash on (barber, date, slot)
        other_client1 = self._fresh_client("1")
        appt_today_future = self.create_appointment(client=other_client1, date=self.today, slot=self.future_time)  # should NOT complete (this will complete if tested at 23:00 because it would become same day but at 00:00 which is before)
        other_client2 = self._fresh_client("2")
        appt_tomorrow = self.create_appointment(client=other_client2, date=self.tomorrow, slot=self.past_time)  # should NOT complete

        # Use different slots for completed/cancelled
        slot_completed = (datetime.datetime.combine(datetime.date.today(), self.past_time) + datetime.timedelta(minutes=1)).time()
        other_client3 = self._fresh_client("3")
        appt_completed = self.create_appointment(client=other_client3, date=self.today, slot=slot_completed, status=AppointmentStatus.COMPLETED.value)
        slot_cancelled = (datetime.datetime.combine(datetime.date.today(), self.past_time) + datetime.timedelta(minutes=2)).time()
        other_client4 = self._fresh_client("4")
        appt_cancelled = self.create_appointment(client=other_client4, date=self.today, slot=slot_cancelled, status=AppointmentStatus.CANCELLED.value)
        
        # runs the task and returns how many updated
        count = complete_ongoing_appointments() 

        
        # Refresh
        appt_yest.refresh_from_db()
        appt_today_past.refresh_from_db()
        appt_today_future.refresh_from_db()
        appt_tomorrow.refresh_from_db()
        appt_completed.refresh_from_db()
        appt_cancelled.refresh_from_db()

        # time part of your mocked "now"
        fake_now_time = fake_now.time() 

        if fake_now_time >= datetime.time(23, 0):
            self.assertEqual(count, 3) # Since time wraps at 00:00, < 00:00 is always False except exactly at 00:00
            self.assertEqual(appt_today_past.status, AppointmentStatus.COMPLETED.value)
            self.assertEqual(appt_today_future.status, AppointmentStatus.COMPLETED.value)

        elif fake_now_time <= datetime.time(1, 0):
            self.assertEqual(count, 1) # Same shit with previous hour, wraps to 23:00 of same day...
            self.assertEqual(appt_today_past.status, AppointmentStatus.ONGOING.value)
            self.assertEqual(appt_today_future.status, AppointmentStatus.ONGOING.value)

        else:
            self.assertEqual(count, 2)  # yest and today_past
            self.assertEqual(appt_today_past.status, AppointmentStatus.COMPLETED.value)
            self.assertEqual(appt_today_future.status, AppointmentStatus.ONGOING.value)


        self.assertEqual(appt_yest.status, AppointmentStatus.COMPLETED.value)
        self.assertEqual(appt_tomorrow.status, AppointmentStatus.ONGOING.value)
        self.assertEqual(appt_completed.status, AppointmentStatus.COMPLETED.value)
        self.assertEqual(appt_cancelled.status, AppointmentStatus.CANCELLED.value)

    
    @patch("api.tasks.timezone")
    def test_send_appointment_reminders_only_targets_window(self, mocked_tz, mock_send_mail):
        """
        Only ONGOING/COMPLETED appts within 1hr window of "now" (and not already reminded) get emails and are flagged.
        """
        # Frozen time: 14:00
        fake_now_naive = datetime.datetime.combine(self.today, datetime.time(14, 0))
        fake_now = timezone.make_aware(fake_now_naive)
        mocked_tz.now.return_value = fake_now
        mocked_tz.localtime.return_value = fake_now
        mocked_tz.make_aware.side_effect = timezone.make_aware
        mocked_tz.get_current_timezone.return_value = timezone.get_current_timezone()

        # For each "today" slot, use distinct clients
        appt_14_30 = self.create_appointment(client=self.client, date=self.today, slot=datetime.time(14, 30))    # should send
        client2 = self._fresh_client("r2")
        appt_15 = self.create_appointment(client=client2, date=self.today, slot=datetime.time(15, 0))        # should send
        client3 = self._fresh_client("r3")
        appt_13 = self.create_appointment(client=client3, date=self.today, slot=datetime.time(13, 0))        # outside (past)
        client4 = self._fresh_client("r4")
        appt_16 = self.create_appointment(client=client4, date=self.today, slot=datetime.time(16, 0))        # outside (future)
        client5 = self._fresh_client("r5")
        appt_tmrw = self.create_appointment(client=client5, date=self.tomorrow, slot=datetime.time(14, 0))   # wrong date
        client6 = self._fresh_client("r6")
        appt_14_15 = self.create_appointment(client=client6, date=self.today, slot=datetime.time(14, 15), reminder_email_sent=True)
        client7 = self._fresh_client("r7")
        appt_cancelled = self.create_appointment(client=client7, date=self.today, slot=datetime.time(14, 45), status=AppointmentStatus.CANCELLED.value)
        # Run task
        send_appointment_reminders()
        # Only the two in window and not already-reminded get flagged
        appt_14_30.refresh_from_db()
        appt_15.refresh_from_db()
        self.assertTrue(appt_14_30.reminder_email_sent)
        self.assertTrue(appt_15.reminder_email_sent)
        # Other NOT updated (check appt_14_15 remains True, others remain False)
        appt_13.refresh_from_db()
        appt_16.refresh_from_db()
        appt_tmrw.refresh_from_db()
        appt_14_15.refresh_from_db()
        appt_cancelled.refresh_from_db()
        self.assertFalse(appt_13.reminder_email_sent)
        self.assertFalse(appt_16.reminder_email_sent)
        self.assertFalse(appt_tmrw.reminder_email_sent)
        self.assertTrue(appt_14_15.reminder_email_sent)
        self.assertFalse(appt_cancelled.reminder_email_sent)

    @patch("api.tasks.timezone")
    def test_send_appointment_reminders_handles_completed_and_ongoing(self, mocked_tz, mock_send_mail):
        """
        Reminder is sent both to ONGOING and COMPLETED (but not CANCELLED, not already-sent).
        """
        fake_now_naive = datetime.datetime.combine(self.today, datetime.time(17, 0))
        fake_now = timezone.make_aware(fake_now_naive)
        mocked_tz.now.return_value = fake_now
        mocked_tz.localtime.return_value = fake_now
        mocked_tz.make_aware.side_effect = timezone.make_aware
        mocked_tz.get_current_timezone.return_value = timezone.get_current_timezone()
        appt_ongoing = self.create_appointment(date=self.today, slot=datetime.time(17, 30), status=AppointmentStatus.ONGOING.value, client=self.client)
        client2 = self._fresh_client("s2")
        appt_completed = self.create_appointment(date=self.today, slot=datetime.time(17, 45), status=AppointmentStatus.COMPLETED.value, client=client2)
        client3 = self._fresh_client("s3")
        appt_cancelled = self.create_appointment(date=self.today, slot=datetime.time(17, 50), status=AppointmentStatus.CANCELLED.value, client=client3)
        send_appointment_reminders()
        # Called for 2 but not third
        appt_ongoing.refresh_from_db()
        appt_completed.refresh_from_db()
        appt_cancelled.refresh_from_db()
        self.assertTrue(appt_ongoing.reminder_email_sent)
        self.assertTrue(appt_completed.reminder_email_sent)
        self.assertFalse(appt_cancelled.reminder_email_sent)

    @patch("api.tasks.timezone")
    def test_send_appointment_reminders_does_not_repeat_or_wrong_status(self, mocked_tz, mock_send_mail):
        """
        Reminder not sent to already-reminded or cancelled or wrong day/status.
        """
        fake_now_naive = datetime.datetime.combine(self.today, datetime.time(15, 0))
        fake_now = timezone.make_aware(fake_now_naive)
        mocked_tz.now.return_value = fake_now
        mocked_tz.localtime.return_value = fake_now
        mocked_tz.make_aware.side_effect = timezone.make_aware
        mocked_tz.get_current_timezone.return_value = timezone.get_current_timezone()
        appt_ok = self.create_appointment(date=self.today, slot=datetime.time(15, 30), status=AppointmentStatus.ONGOING.value, client=self.client)
        client2 = self._fresh_client("s4")
        appt_sent = self.create_appointment(date=self.today, slot=datetime.time(15, 40), status=AppointmentStatus.ONGOING.value, reminder_email_sent=True, client=client2)
        client3 = self._fresh_client("s5")
        appt_cancel = self.create_appointment(date=self.today, slot=datetime.time(15, 45), status=AppointmentStatus.CANCELLED.value, client=client3)
        client4 = self._fresh_client("s6")
        appt_not_today = self.create_appointment(date=self.tomorrow, slot=datetime.time(15, 30), status=AppointmentStatus.ONGOING.value, client=client4)
        send_appointment_reminders()
        # Only appt_ok gets reminder
        appt_ok.refresh_from_db()
        appt_sent.refresh_from_db()
        appt_cancel.refresh_from_db()
        appt_not_today.refresh_from_db()
        self.assertTrue(appt_ok.reminder_email_sent)
        self.assertTrue(appt_sent.reminder_email_sent)
        self.assertFalse(appt_cancel.reminder_email_sent)
        self.assertFalse(appt_not_today.reminder_email_sent)