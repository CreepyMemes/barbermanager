import datetime
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import (
    Barber,
    Client,
    Service,
    AppointmentService,
    Availability,
    Appointment,
    Review,
    AppointmentStatus,
    Roles
)

class ClientProfileTest(APITestCase):
    """
    Tests for the client profile management and appointment/review endpoints.
    """

    def setUp(self):
        # Endpoint URLs
        self.login_url = reverse("login_user")
        self.profile_url = reverse("manage_client_profile")
        self.appointments_url = reverse("get_client_appointments")
        self.reviews_url = reverse("get_client_reviews")

        # Create Users
        self.barber_password = "BarberPass123!"
        self.barber_user = Barber.objects.create_user(
            username="barberA",
            email="barb@abc.com",
            password=self.barber_password,
            name="BarbName",
            surname="BarbSurname",
        )

        self.client_password = "ClientPwd123!"
        self.client_user = Client.objects.create_user(
            username="johndoe_",
            email="user@abc.com",
            password=self.client_password,
            name="John",
            surname="Doe",
            phone_number="+12025551234",
        )

        self.client_user_other = Client.objects.create_user( # For "not-owner" checks
            username="jane",
            email="jane@abc.com",
            password="OtherPwd123!",
            name="Jane",
            surname="Doe",
        )

        self.barber_user_other = Client.objects.create_user( # For "not-owner" checks
            username="barbone",
            email="barbo@abc.com",
            password="OtherBestPwd123!",
            name="Rock",
            surname="Bottom",
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

    def login_as_client(self):
        """
        Authenticate as the test client.
        """
        resp = self.client.post(self.login_url, {"username": self.client_user.username, "password": self.client_password}, format="json")
        token = resp.data["token"]["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


    def login_as_barber(self):
        """
        Authenticate as a test barber (not a client).
        """
        resp = self.client.post(self.login_url, {"username": self.barber_user.username, "password": self.barber_password}, format="json")
        token = resp.data["token"]["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


    def test_get_profile_success(self):
        """
        Authenticated client can get their full profile including appointments and reviews.
        """
        self.login_as_client()

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile = response.data["profile"]
        self.assertEqual(profile, self.client_user.to_dict())
        self.assertEqual(profile['role'], Roles.CLIENT.value)


    def test_get_profile_requires_auth_and_client_role(self):
        """
        Getting profile requires client authentication; returns 403 for non-clients.
        """
        # Not authenticated
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Auth as barber, not client
        self.login_as_barber()

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_profile_success_partial(self):
        """
        Client can update part(s) of their profile.
        """
        self.login_as_client()
        patch = {"username": "newclientname", "name": "CName", "surname": "CSurname", "phone_number": "+15715550111"}
        resp = self.client.patch(self.profile_url, patch, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["detail"], "Profile info updated successfully.")
        self.client_user.refresh_from_db()
        self.assertEqual(self.client_user.username, patch["username"])
        self.assertEqual(self.client_user.name, patch["name"])
        self.assertEqual(self.client_user.surname, patch["surname"])
        self.assertEqual(self.client_user.phone_number, patch["phone_number"])


    def test_update_profile_username_unique_constraint(self):
        """
        Username cannot be changed to one in use.
        """
        # Make "jane" also a taken username
        self.login_as_client()
        response = self.client.patch(self.profile_url, {"username": "jane"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("taken", str(response.data["detail"]).lower())


    def test_update_profile_requires_field(self):
        """
        Updating profile with no fields returns validation error.
        """
        self.login_as_client()
        resp = self.client.patch(self.profile_url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("must provide at least one field", str(resp.data["detail"]))


    def test_update_profile_phone_number_invalid(self):
        """
        Invalid phone number format is not accepted.
        """
        self.login_as_client()
        resp = self.client.patch(self.profile_url, {"phone_number": "123abc"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone number must be entered", str(resp.data["phone_number"][0]).lower())


    def test_delete_profile_success(self):
        """
        Client can delete their profile.
        """
        self.login_as_client()
        resp = self.client.delete(self.profile_url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(pk=self.client_user.pk).exists())


    def test_list_appointments(self):
        """
        Client can list all their appointments.
        """
        s1 = Service.objects.create(barber=self.barber_user, name="Hair", price=10)
        app_1 = Appointment.objects.create(
            client=self.client_user, barber=self.barber_user,
            date=datetime.date.today(), slot=datetime.time(10, 0),
            status=AppointmentStatus.ONGOING.value,
        )
        self.add_services(app_1, [s1])

        app_2 = Appointment.objects.create(
            client=self.client_user, barber=self.barber_user,
            date=datetime.date.today() + datetime.timedelta(days=1), slot=datetime.time(11, 0),
            status=AppointmentStatus.COMPLETED.value,
        )
        self.add_services(app_2, [s1])

        self.login_as_client()
        resp = self.client.get(self.appointments_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data["appointments"]), 2)
        self.assertTrue(any(app["id"] == app_1.id for app in resp.data["appointments"]))


    def test_list_appointments_requires_auth_client(self):
        """
        Only authenticated clients may list appointments.
        """
        resp = self.client.get(self.appointments_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.login_as_barber()
        resp2 = self.client.get(self.appointments_url)
        self.assertEqual(resp2.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_appointment_success(self):
        """
        Client can create a valid appointment with a barber and services.
        """
        service_1 = Service.objects.create(
            barber=self.barber_user, 
            name="Haircut", 
            price=10
        )

        service_2 = Service.objects.create(
            barber=self.barber_user, 
            name="Shave", 
            price=15
        )

        Availability.objects.create(
            barber=self.barber_user, 
            date=datetime.date.today(), 
            slots=["09:00", "11:00"]
        )

        self.login_as_client()

        url = reverse("create_client_appointment", kwargs={"barber_id": self.barber_user.id})

        data = {
            "date": datetime.date.today(),
            "slot": "09:00",
            "services": [service_1.id, service_2.id],
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("Appointment added successfully", response.data["detail"])

        appointment = Appointment.objects.get(client=self.client_user)

        self.assertEqual(appointment.barber, self.barber_user)
        self.assertEqual(str(appointment.date), str(datetime.date.today()))
        self.assertEqual([x.id for x in appointment.services.all()], [service_1.id, service_2.id])


    def test_create_appointment_requires_barber_exists(self):
        """
        Cannot create appointment with non-existent, inactive, or wrong barber.
        """
        self.login_as_client()
        url = reverse("create_client_appointment", kwargs={"barber_id": 9999})
        data = {
            "date": datetime.date.today(),
            "slot": "09:00",
            "services": [],
        }
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp.data["detail"]).lower())


    def test_create_appointment_rejects_conflicts(self):
        """
        Rejects double bookings for same client/date or same barber/slot or ongoing.
        """
        service_1 = Service.objects.create(barber=self.barber_user, name="Cut", price=9)
        today = datetime.date.today()
        slot = datetime.time(9, 0)
        # Set available
        Availability.objects.create(barber=self.barber_user, date=today, slots=["09:00"])

        # Prior appointment (ONGOING for client)
        appointment = Appointment.objects.create(
            client=self.client_user, 
            barber=self.barber_user, 
            date=today, 
            slot=slot,
            status=AppointmentStatus.ONGOING.value
        )
        AppointmentService.objects.create(
            appointment=appointment,
            name=service_1.name,
            price=service_1.price,
            original_service=service_1
        )

        self.login_as_client()
        url = reverse("create_client_appointment", kwargs={"barber_id": self.barber_user.id})
        data = {
            "date": today,
            "slot": "09:00",
            "services": [service_1.id],
        }
        # Should fail: client already has ONGOING appt
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already has an ONGOING appointment".lower(), str(resp.data["detail"]).lower())


    def test_create_appointment_rejects_wrong_service(self):
        """
        Cannot create appointment with a service not provided by the barber.
        """
        their_barber = Barber.objects.create_user(
            username="otherbarber", email="x@x.com", password="p", name="t", surname="t",
            is_active=True
        )
        s_other = Service.objects.create(barber=their_barber, name="Wax", price=10)
        s_our = Service.objects.create(barber=self.barber_user, name="Buzz", price=9)
        dt = datetime.date.today()
        Availability.objects.create(barber=self.barber_user, date=dt, slots=["13:00"])
        self.login_as_client()
        url = reverse("create_client_appointment", kwargs={"barber_id": self.barber_user.id})
        data = {
            "date": dt,
            "slot": "13:00",
            "services": [s_other.id],  # not from this barber!
        }
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp.data["detail"]))


    def test_create_appointment_rejects_if_unavailable(self):
        """
        Cannot create appointment if barber not available (no availability or slot missing).
        """
        s1 = Service.objects.create(barber=self.barber_user, name="Mass", price=8)
        dt = datetime.date.today()
        # No Availability for barber
        self.login_as_client()
        url = reverse("create_client_appointment", kwargs={"barber_id": self.barber_user.id})
        data = {
            "date": dt,
            "slot": "08:00",  # not available
            "services": [s1.id],
        }
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("not available", str(resp.data["detail"]).lower())

        Availability.objects.create(barber=self.barber_user, date=dt, slots=["13:00"])
        # Now date exists, but slot is missing
        data["slot"] = "08:00"
        resp2 = self.client.post(url, data, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("not available", str(resp2.data["detail"]).lower())


    def test_cancel_appointment_success(self):
        """
        Client can cancel their ONGOING appointment.
        """
        s1 = Service.objects.create(barber=self.barber_user, name="B", price=7)
        appt = Appointment.objects.create(
            client=self.client_user, 
            barber=self.barber_user,
            date=datetime.date.today(), 
            slot=datetime.time(8,0),
            status=AppointmentStatus.ONGOING.value
        )
        self.add_services(appt, [s1])

        self.login_as_client()
        url = reverse("delete_client_appointment", kwargs={"appointment_id": appt.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        appt.refresh_from_db()
        self.assertEqual(appt.status, AppointmentStatus.CANCELLED.value)


    def test_cancel_appointment_not_found_or_not_ongoing(self):
        """
        Only ONGOING appts can be cancelled; not found or wrong client returns error.
        """
        s1 = Service.objects.create(barber=self.barber_user, name="V", price=5)
        appt = Appointment.objects.create(
            client=self.client_user, barber=self.barber_user,
            date=datetime.date.today(), slot=datetime.time(8,0),
            status=AppointmentStatus.COMPLETED.value
        )
        self.add_services(appt, [s1])

        self.login_as_client()
        # Not ONGOING
        url = reverse("delete_client_appointment", kwargs={"appointment_id": appt.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Only ONGOING appointments can be cancelled", str(resp.data["detail"]))

        # Not your appointment
        appt2 = Appointment.objects.create(
            client=self.client_user_other, barber=self.barber_user,
            date=datetime.date.today(), slot=datetime.time(9,0),
            status=AppointmentStatus.ONGOING.value
        )
        self.add_services(appt2, [s1])

        url2 = reverse("delete_client_appointment", kwargs={"appointment_id": appt2.id})
        resp2 = self.client.delete(url2)
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp2.data["detail"]))


    def test_list_reviews(self):
        """
        Client can list all the reviews they've posted.
        """
        # Need at least one completed appointment and review created
        service_1 = Service.objects.create(barber=self.barber_user, name="BE", price=6)
        appointment = Appointment.objects.create(
            client=self.client_user, 
            barber=self.barber_user,
            date=datetime.date.today(), 
            slot=datetime.time(22,0),
            status=AppointmentStatus.COMPLETED.value
        )
        self.add_services(appointment, [service_1])
        
        review = Review.objects.create(
            client=self.client_user, 
            barber=self.barber_user, 
            rating=4, 
            comment="Nice cut!"
        )
        self.login_as_client()
        resp = self.client.get(self.reviews_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(any(r["id"] == review.id for r in resp.data["reviews"]))
        self.assertEqual(resp.data["reviews"][0]["comment"], "Nice cut!")


    def test_list_reviews_requires_client_only(self):
        """
        Only clients can list their reviews.
        """
        resp = self.client.get(self.reviews_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.login_as_barber()
        resp2 = self.client.get(self.reviews_url)
        self.assertEqual(resp2.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_review_success(self):
        """
        Client can create a review on a completed appointment (appointment->barber).
        """
        s1 = Service.objects.create(barber=self.barber_user, name="Mow", price=10)
        appt = Appointment.objects.create(
            client=self.client_user, 
            barber=self.barber_user,
            date=datetime.date.today(), 
            slot=datetime.time(12,0),
            status=AppointmentStatus.COMPLETED.value
        )
        self.add_services(appt, [s1])
        
        self.login_as_client()
        url = reverse("create_client_review", kwargs={"barber_id": self.barber_user.id})
        data = {"rating": 5, "comment": "Spectacular"}
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        review = Review.objects.get(client=self.client_user, barber=self.barber_user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Spectacular")


    def test_create_review_fail_non_completed_appointment(self):
        """
        Cannot review a non-completed appointment.
        """
        s1 = Service.objects.create(barber=self.barber_user, name="Face", price=6)
        appt = Appointment.objects.create(
            client=self.client_user, 
            barber=self.barber_user,
            date=datetime.date.today(), 
            slot=datetime.time(15,0),
            status=AppointmentStatus.ONGOING.value
        )
        self.add_services(appt, [s1])

        
        self.login_as_client()
        url = reverse("create_client_review", kwargs={"barber_id": self.barber_user.id})
        resp = self.client.post(url, {"rating": 4, "comment": ""}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ou may only review a barber if you have completed at least one appointment with them.", str(resp.data["detail"]))


    def test_create_review_cannot_duplicate(self):
        """
        Client can only review a given barber once.
        """
        s1 = Service.objects.create(barber=self.barber_user, name="Legs", price=6)
        completed = Appointment.objects.create(
            client=self.client_user, barber=self.barber_user,
            date=datetime.date.today(), slot=datetime.time(17,0),
            status=AppointmentStatus.COMPLETED.value
        )
        self.add_services(completed, [s1])
        
        review = Review.objects.create(
            client=self.client_user, 
            barber=self.barber_user, 
            rating=3, 
            comment="zzz"
        )

        self.login_as_client()
        url = reverse("create_client_review", kwargs={"barber_id": self.barber_user.id})
        resp = self.client.post(url, {"rating": 5, "comment": ""}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("review for the barber", str(resp.data["detail"]))


    def test_create_review_fail_wrong_barber(self):
        """
        Can only review your own appointments.
        """
        self.login_as_client()
        url = reverse("create_client_review", kwargs={"barber_id": self.barber_user_other.id})
        resp = self.client.post(url, {"rating": 2, "comment": ""}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp.data["detail"]))


    def test_update_review_success(self):
        """
        Client can update their own review's rating/comment.
        """
        service_1 = Service.objects.create(barber=self.barber_user, name="BU", price=1)
        appointment = Appointment.objects.create(
            client=self.client_user, 
            barber=self.barber_user,
            date=datetime.date.today(), 
            slot=datetime.time(20,0),
            status=AppointmentStatus.COMPLETED.value
        )
        self.add_services(appointment, [service_1])

        review = Review.objects.create(
            client=self.client_user, 
            barber=self.barber_user, 
            rating=3, 
            comment="Old comment"
        )
        self.login_as_client()
        url = reverse("manage_client_reviews", kwargs={"review_id": review.id})
        resp = self.client.patch(url, {"rating": 2, "comment": "Better"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.rating, 2)
        self.assertEqual(review.comment, "Better")
        self.assertIsNotNone(review.edited_at)


    def test_update_review_requires_field(self):
        """
        Cannot update a review with no fields specified.
        """
        service_1 = Service.objects.create(barber=self.barber_user, name="XY", price=8)
        appointment = Appointment.objects.create(
            client=self.client_user, 
            barber=self.barber_user,
            date=datetime.date.today(), 
            slot=datetime.time(18,0),
            status=AppointmentStatus.COMPLETED.value
        )
        self.add_services(appointment, [service_1])

        review = Review.objects.create(
            client=self.client_user, 
            barber=self.barber_user, 
            rating=2, 
            comment="hi"
        )

        self.login_as_client()
        url = reverse("manage_client_reviews", kwargs={"review_id": review.id})

        response = self.client.patch(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("at least one field", str(response.data["detail"]))


    def test_update_review_not_found(self):
        """
        Cannot update a review not owned or not found.
        """
        self.login_as_client()
        url = reverse("manage_client_reviews", kwargs={"review_id": 9999})
        resp = self.client.patch(url, {"rating": 4}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp.data["detail"]))


    def test_delete_review_success(self):
        """
        Client can delete their review.
        """
        service_1 = Service.objects.create(barber=self.barber_user, name="XC", price=4)
        appointment = Appointment.objects.create(
            client=self.client_user, 
            barber=self.barber_user,
            date=datetime.date.today(), 
            slot=datetime.time(19,0),
            status=AppointmentStatus.COMPLETED.value
        )
        self.add_services(appointment, [service_1])

        review = Review.objects.create(
            client=self.client_user, 
            barber=self.barber_user, 
            rating=1, 
            comment="x"
        )
        self.login_as_client()
        url = reverse("manage_client_reviews", kwargs={"review_id": review.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(pk=review.id).exists())


    def test_delete_review_not_found(self):
        """
        Fails gracefully when deleting a review that does not exist or not owned.
        """
        self.login_as_client()
        url = reverse("manage_client_reviews", kwargs={"review_id": 34901})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp.data["detail"]))