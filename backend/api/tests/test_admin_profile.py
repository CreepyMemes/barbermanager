import datetime
from decimal import Decimal
from django.urls import reverse
from django.core import mail
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import (
    User,
    Admin,
    Barber,
    Client,
    Service,
    Availability,
    Appointment,
    Review,
    AppointmentStatus,
    Roles,
)

class AdminProfileTest(APITestCase):
    """
    Tests for all admin features, profile getter, barber and availabilities management, statistics generation.
    """
    def setUp(self):
        # Endpoint URLs
        self.profile_url = reverse("get_admin_profile")
        self.invite_url = reverse("invite_barber")  # POST
        # Delete barber, create availability, manage availability use arg URLs
        self.statistics_url = reverse("get_admin_statistics")
        self.all_appointments_url = reverse("get_all_appointments")
        # Create test admin
        self.admin_password = "AdminPass321!"
        self.admin = Admin.objects.create_user(
            username="adminuser",
            password=self.admin_password,
            email="admin@email.com",
            is_active=True,
        )
        self.admin.refresh_from_db()
        self.admin.role = Roles.ADMIN.value
        self.admin.is_staff = True
        self.admin.is_superuser = True
        self.admin.save()
        # Create a sample barber (active) and one inactive for some tests
        self.barber = Barber.objects.create_user(
            username="barby",
            password="BarberXPass!",
            email="barber@email.com",
            name="Bob",
            surname="Ross",
            is_active=True,
        )
        self.barber_inactive = Barber.objects.create_user(
            username="barbinactive",
            password="ZZdummy12",
            email="inactive@email.com",
            name="Inactive",
            surname="Barb",
            is_active=False,
        )
        # Make a client
        self.client_user = Client.objects.create_user(
            username="clnt",
            password="ClientPw11",
            email="client@x.com",
            name="Cilla",
            surname="User",
            is_active=True,
        )


    def login_as_admin(self):
        resp = self.client.post(
            reverse("login_user"),
            {"username": self.admin.username, "password": self.admin_password},
            format="json",
        )
        token = resp.data["token"]["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


    def login_as_client(self):
        resp = self.client.post(
            reverse("login_user"),
            {"username": self.client_user.username, "password": "ClientPw11"},
            format="json",
        )
        token = resp.data["token"]["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


    def test_get_admin_profile_success(self):
        """
        Admin can fetch their profile, and sees all barbers, appointments, and reviews.
        """
        # Setup some barbers, appointments, reviews to show up in list
        Service.objects.create(barber=self.barber, name="Haircut", price=Decimal("22"))
        appt = Appointment.objects.create(
            client=self.client_user,
            barber=self.barber,
            date=datetime.date.today(),
            slot=datetime.time(12, 30),
            status=AppointmentStatus.ONGOING.value,
        )
        Review.objects.create(
            appointment=appt,
            client=self.client_user,
            barber=self.barber,
            rating=4,
            comment="Nice cut",
        )
        self.login_as_admin()
        resp = self.client.get(self.profile_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["id"], self.admin.id)
        self.assertEqual(resp.data["role"], Roles.ADMIN.value)
        # "barbers" is a list with detailed barbers, including the test ones
        barber_ids = [b["id"] for b in resp.data["barbers"]]
        self.assertIn(self.barber.id, barber_ids)
        # "appointments" and "reviews" lists exist
        self.assertTrue(isinstance(resp.data["appointments"], list))
        self.assertTrue(isinstance(resp.data["reviews"], list))


    def test_get_admin_profile_requires_admin(self):
        """
        Only admins can access profile admin endpoint (403/401 otherwise).
        """
        # Not authenticated at all
        resp = self.client.get(self.profile_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.login_as_client()
        resp = self.client.get(self.profile_url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


    def test_invite_barber_success(self):
        """
        Admin can invite a barber via email: creates inactive user, sends invite.
        """
        self.login_as_admin()
        email = "newbarb@nowhere.com"
        response = self.client.post(self.invite_url, {"email": email}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Barber invited successfully", response.data["detail"])

        # Barber should now exist, inactive
        newbarber = Barber.objects.get(email=email)
        self.assertFalse(newbarber.is_active)
        
        # Email send side effect: should have been called (if using real mail system)
        self.assertGreaterEqual(len(mail.outbox), 1)
        self.assertIn(email, mail.outbox[-1].to)



    def test_invite_barber_existing_email(self):
        """
        Fails if trying to invite using an email already registered.
        """
        self.login_as_admin()
        resp = self.client.post(self.invite_url, {"email": self.barber.email}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already taken", str(resp.data["detail"]))


    def test_invite_barber_requires_admin(self):
        """
        Only admin can invite barbers.
        """
        resp = self.client.post(self.invite_url, {"email": "who@foo.com"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.login_as_client()
        resp = self.client.post(self.invite_url, {"email": "some@b.com"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_barber_success(self):
        """
        Admin can delete an active barber by id.
        """
        self.login_as_admin()
        url = reverse("delete_barber", kwargs={"barber_id": self.barber.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Barber.objects.filter(pk=self.barber.pk).exists())


    def test_delete_barber_not_found(self):
        """
        Returns error if barber does not exist.
        """
        self.login_as_admin()
        url = reverse("delete_barber", kwargs={"barber_id": 99991})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp.data["id"][0]))


    def test_delete_barber_inactive(self):
        """
        Cannot delete an inactive barber (validation error).
        """
        self.login_as_admin()
        url = reverse("delete_barber", kwargs={"barber_id": self.barber_inactive.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("not active", str(resp.data["id"][0]))


    def test_delete_barber_requires_admin(self):
        """
        Only admins can delete barbers.
        """
        url = reverse("delete_barber", kwargs={"barber_id": self.barber.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.login_as_client()
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_availability_success(self):
        """
        Admin can create a barber's availability for a date/slots.
        """
        self.login_as_admin()
        url = reverse("create_barber_availability", kwargs={"barber_id": self.barber.id})
        today = datetime.date.today()
        slots = ["10:00", "11:00"]
        slots_as_times = [datetime.time(int(s.split(":")[0]), int(s.split(":")[1])) for s in slots]
        resp = self.client.post(
            url, {"date": str(today), "slots": slots}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn("created successfully", resp.data["detail"])
        self.assertTrue(Availability.objects.filter(barber=self.barber, date=today).exists())
        avail = Availability.objects.get(barber=self.barber, date=today)
        self.assertEqual(sorted(avail.slots), sorted(slots))


    def test_create_availability_duplicate(self):
        """
        Cannot create two availabilities for same barber and date.
        """
        today = datetime.date.today()
        Availability.objects.create(barber=self.barber, date=today, slots=["09:00"])
        self.login_as_admin()
        url = reverse("create_barber_availability", kwargs={"barber_id": self.barber.id})
        resp = self.client.post(
            url, {"date": str(today), "slots": ["10:00"]}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already exists", str(resp.data["detail"]))


    def test_create_availability_requires_admin(self):
        """
        Only admins may create availabilities for barbers.
        """
        url = reverse("create_barber_availability", kwargs={"barber_id": self.barber.id})
        today = datetime.date.today()
        data = {"date": str(today), "slots": ["13:00"]}
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.login_as_client()
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_availability_success(self):
        """
        Admin can patch date or slots of an availability by id.
        """
        avail = Availability.objects.create(
            barber=self.barber, date=datetime.date.today(), slots=["09:30"]
        )
        new_slots = ["10:30", "11:30"]
        self.login_as_admin()
        url = reverse(
            "manage_barber_availability",
            kwargs={"barber_id": self.barber.id, "availability_id": avail.id},
        )
        resp = self.client.patch(url, {"slots": new_slots}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        avail.refresh_from_db()
        self.assertEqual(sorted(avail.slots), sorted(new_slots))


    def test_update_availability_not_found(self):
        """
        Returns error if availability does not exist for given barber+id.
        """
        self.login_as_admin()
        url = reverse(
            "manage_barber_availability",
            kwargs={"barber_id": self.barber.id, "availability_id": 99994},
        )
        resp = self.client.patch(url, {"slots": ["10:00"]}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp.data["detail"]))


    def test_update_availability_duplicate_date(self):
        """
        Patch to a date that already has another availability for this barber is rejected.
        """
        a1 = Availability.objects.create(barber=self.barber, date=datetime.date.today(), slots=["09:00"])
        a2 = Availability.objects.create(barber=self.barber, date=datetime.date.today() + datetime.timedelta(days=1), slots=["08:00"])
        self.login_as_admin()
        url = reverse(
            "manage_barber_availability", kwargs={"barber_id": self.barber.id, "availability_id": a2.id}
        )
        resp = self.client.patch(
            url, {"date": str(datetime.date.today())}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already exists", str(resp.data["detail"]))


    def test_update_availability_requires_field(self):
        """
        At least one of date/slots is required for PATCH.
        """
        avail = Availability.objects.create(
            barber=self.barber, date=datetime.date.today(), slots=["09:00"]
        )
        self.login_as_admin()
        url = reverse(
            "manage_barber_availability",
            kwargs={"barber_id": self.barber.id, "availability_id": avail.id},
        )
        resp = self.client.patch(url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("at least one field", str(resp.data["detail"]))


    def test_delete_availability_success(self):
        """
        Admin can delete a barber's availability by id.
        """
        avail = Availability.objects.create(
            barber=self.barber, date=datetime.date.today(), slots=["09:40"]
        )
        self.login_as_admin()
        url = reverse(
            "manage_barber_availability",
            kwargs={"barber_id": self.barber.id, "availability_id": avail.id},
        )
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Availability.objects.filter(pk=avail.id).exists())


    def test_delete_availability_not_found(self):
        """
        Returns error if availability does not exist.
        """
        self.login_as_admin()
        url = reverse(
            "manage_barber_availability",
            kwargs={"barber_id": self.barber.id, "availability_id": 123213},
        )
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp.data["detail"]))


    def test_admin_statistics(self):
        """
        Admin receives correct statistics (appointments, reviews, revenue, average rating).
        """
        # Populate system with data
        service = Service.objects.create(barber=self.barber, name="Buzz", price=Decimal("35.00"))
        appt1 = Appointment.objects.create(
            client=self.client_user, barber=self.barber,
            date=datetime.date.today(), slot=datetime.time(14, 0),
            status=AppointmentStatus.COMPLETED.value
        )
        appt1.services.add(service)
        appt2 = Appointment.objects.create(
            client=self.client_user, barber=self.barber,
            date=datetime.date.today(), slot=datetime.time(15, 0),
            status=AppointmentStatus.CANCELLED.value
        )
        # Only COMPLETED with actual service counts for revenue
        Review.objects.create(appointment=appt1, client=self.client_user, barber=self.barber, rating=5, comment="top!")
        self.login_as_admin()
        resp = self.client.get(self.statistics_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        stats = resp.data["statistics"]
        self.assertEqual(stats["total_appointments"], 2)
        self.assertEqual(float(stats["total_revenue"]), 35.0)
        self.assertEqual(stats["total_reviews"], 1)
        self.assertAlmostEqual(float(stats["average_rating"]), 5.0, places=1)


    def test_admin_get_all_appointments(self):
        """
        Admin can fetch all system appointments: should include all records.
        """
        s1 = Service.objects.create(barber=self.barber, name="Trim", price=20)
        a1 = Appointment.objects.create(
            client=self.client_user, barber=self.barber,
            date=datetime.date.today(), slot=datetime.time(9, 0),
            status=AppointmentStatus.COMPLETED.value
        )
        a1.services.add(s1)
        self.login_as_admin()
        resp = self.client.get(self.all_appointments_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("appointments", resp.data)
        self.assertTrue(any(a["id"] == a1.id for a in resp.data["appointments"]))