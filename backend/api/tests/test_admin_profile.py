import datetime
from decimal import Decimal
from django.urls import reverse
from django.core import mail
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import (
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
        self.invite_url = reverse("invite_barber")
        self.get_all_barbers = reverse("get_all_barbers")
        self.get_all_clients = reverse("get_all_clients")
        self.all_appointments_url = reverse("get_all_appointments")

        # Create test admin
        self.admin_password = "AdminPass321!"
        self.admin_username = "adminuser"
        self.admin = Admin.objects.create_superuser(
            username=self.admin_username,
            password=self.admin_password,
        )

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
        Admin can fetch their profile, and sees all statistics on their dashboard.
        """
        service_1 = Service.objects.create(
            barber=self.barber, 
            name="Haircut", 
            price=Decimal("5.5")
        )

        service_2 = Service.objects.create(
            barber=self.barber, 
            name="Buzz", 
            price=Decimal("10.00")
        )

        # Create cancelled appointment
        appointment_1 = Appointment.objects.create(
            client=self.client_user,
            barber=self.barber,
            date=datetime.date.today(),
            slot=datetime.time(12, 0),
            status=AppointmentStatus.CANCELLED.value,
        )
        appointment_1.services.add(service_1, service_2)

        # Create appointment same day as cancelled one
        appointment_2 = Appointment.objects.create(
            client=self.client_user, 
            barber=self.barber,
            date=datetime.date.today() ,
            slot=datetime.time(14, 0),
            status=AppointmentStatus.COMPLETED.value,
        )
        appointment_2.services.add(service_1, service_2)

        # Create completed appointment on another day
        appointment_3 = Appointment.objects.create(
            client=self.client_user, 
            barber=self.barber,
            date=datetime.date.today() + datetime.timedelta(days=1), 
            slot=datetime.time(14, 0),
            status=AppointmentStatus.COMPLETED.value,
        )
        appointment_3.services.add(service_2)
        
        # Create ongoing appointment on another day
        appointment_4 = Appointment.objects.create(
            client=self.client_user, 
            barber=self.barber,
            date=datetime.date.today() + datetime.timedelta(days=2),
            slot=datetime.time(15, 0),
            status=AppointmentStatus.ONGOING.value,
        )
        appointment_4.services.add(service_2)
        
        # Create reveiw for completed appointment
        Review.objects.create(
            appointment=appointment_2, 
            client=self.client_user, 
            barber=self.barber, 
            rating=5, 
            comment="top!"
        )

        # Create another client
        client_1 = Client.objects.create_user(
            username="testerclient",
            password="sugomadic",
            email="clients@xxx.com",
            name="Bomber",
            surname="Romber",
            is_active=True,
        )

        # Create another barber
        barber_1 = Barber.objects.create_user(
            username="testerbarber",
            password="ligmabals",
            email="barbers@xxx.com",
            name="Dudong",
            surname="Sorcer",
            is_active=True,
        )

        # Create appointment by another client
        appointment_5 = Appointment.objects.create(
            client=client_1, 
            barber=barber_1,
            date=datetime.date.today(),
            slot=datetime.time(14, 0),
            status=AppointmentStatus.COMPLETED.value,
        )
        appointment_5.services.add(service_2)

        # Create reveiw by another client
        Review.objects.create(
            appointment=appointment_5, 
            client=client_1, 
            barber=self.barber, 
            rating=2, 
            comment="trash..."
        )

        self.login_as_admin()

        response = self.client.get(self.profile_url)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile = response.data["profile"]
        self.assertEqual(profile, self.admin.to_dict())
        self.assertEqual(profile['role'], Roles.ADMIN.value)
        

    def test_get_admin_profile_requires_admin(self):
        """
        Only admins can access profile admin endpoint (403/401 otherwise).
        """
        # Not authenticated at all
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.login_as_client()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_barbers_list_success(self):
        """
        Return a list of all barbers to authenticated admin
        """
        self.login_as_admin()

        response = self.client.get(self.get_all_barbers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        barbers = response.data["barbers"]
        self.assertIn(self.barber.to_dict(), barbers)
        self.assertIn(self.barber_inactive.to_dict(), barbers)


    def test_get_clients_list_success(self):
        """
        Return a list of all clients to authenticated admin
        """

        # Create another client
        client_1 = Client.objects.create_user(
            username="testerclient",
            password="sugomadic",
            email="clients@xxx.com",
            name="Bomber",
            surname="Romber",
            is_active=True,
        )

        self.login_as_admin()

        response = self.client.get(self.get_all_clients)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        clients = response.data["clients"]
        self.assertIn(self.client_user.to_dict(), clients)
        self.assertIn(client_1.to_dict(), clients)


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
        availability = Availability.objects.create(
            barber=self.barber, 
            date=datetime.date.today(), 
            slots=["09:30"]
        )

        new_slots = ["10:30", "11:30"]
        new_date = datetime.date.today() + datetime.timedelta(days=1)

        self.login_as_admin()

        url = reverse("manage_barber_availability", kwargs={"barber_id": self.barber.id, "availability_id": availability.id})
        
        response = self.client.patch(url, {"slots": new_slots, "date": new_date}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        availability.refresh_from_db()
        self.assertEqual(availability.date, new_date)
        self.assertEqual(sorted(availability.slots), sorted(new_slots))


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


    def test_admin_get_all_appointments(self):
        """
        Admin can fetch all system appointments: should include all records.
        """
        service_1 = Service.objects.create(
            barber=self.barber, 
            name="Trim", 
            price=20
        )
        appointment_1 = Appointment.objects.create(
            client=self.client_user, barber=self.barber,
            date=datetime.date.today(), slot=datetime.time(9, 0),
            status=AppointmentStatus.COMPLETED.value
        )
        appointment_1.services.add(service_1)

        self.login_as_admin()

        response = self.client.get(self.all_appointments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("appointments", response.data)
        self.assertTrue(any(a["id"] == appointment_1.id for a in response.data["appointments"]))