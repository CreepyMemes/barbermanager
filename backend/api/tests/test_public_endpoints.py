import datetime
from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import (
    Barber,
    Service,
    Availability,
    Appointment,
    Client,
    Review,
    AppointmentStatus,
    Roles
)

class PublicEndpointsTest(APITestCase):
    """
    Tests for public access to barber listings, barbers' profiles, availabilities, and services.
    """

    def setUp(self):
        # Create barbers (active and inactive), barbers with and without description
        self.barber1 = Barber.objects.create_user(
            username="barber_one",
            email="barber1@barbershop.com",
            password="pw",
            name="B1",
            surname="One",
            description="Master barber",
            is_active=True
        )
        self.barber2 = Barber.objects.create_user(
            username="barber_two",
            email="barber2@barbershop.com",
            password="pw",
            name="B2",
            surname="Two",
            description="",
            is_active=True
        )
        self.barber_inactive = Barber.objects.create_user(
            username="hidden",
            email="hidden@barbershop.com",
            password="pw",
            name="Ghost",
            surname="User",
            is_active=False
        )
        # Services and availabilities
        self.service1 = Service.objects.create(barber=self.barber1, name="Fade", price=Decimal("25.00"))
        self.service2 = Service.objects.create(barber=self.barber1, name="Lineup", price=Decimal("10.00"))
        self.service3 = Service.objects.create(barber=self.barber2, name="Kids Cut", price=Decimal("15.00"))
        self.today = datetime.date.today()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.availability1 = Availability.objects.create(barber=self.barber1, date=self.today, slots=["09:00", "10:00"])
        self.availability2 = Availability.objects.create(barber=self.barber1, date=self.tomorrow, slots=["16:00"])
        self.availability3 = Availability.objects.create(barber=self.barber2, date=self.today, slots=["12:00"])
        # Clients and reviews for public profile demo
        self.client_user = Client.objects.create_user(
            username="c",
            email="c@foo.com",
            password="wo",
            name="C",
            surname="Bar",
            is_active=True
        )
        self.appointment = Appointment.objects.create(
            client=self.client_user,
            barber=self.barber1,
            date=self.today,
            slot=datetime.time(9, 0),
            status=AppointmentStatus.COMPLETED.value
        )
        self.appointment.services.set([self.service1])
        self.review = Review.objects.create(
            appointment=self.appointment,
            client=self.client_user,
            barber=self.barber1,
            rating=4,
            comment="Awesome cut!"
        )
        # Endpoints
        self.barber_list_url = reverse("get_barbers_list")
        self.barber_1_profile_url = reverse("get_barber_profile_public", kwargs={'barber_id': self.barber1.id})
        self.barber_2_profile_url = reverse("get_barber_profile_public", kwargs={'barber_id': self.barber2.id})
        self.barber_1_avail_url = reverse("get_barber_availabilities_public", kwargs={'barber_id': self.barber1.id})
        self.barber_2_avail_url = reverse("get_barber_availabilities_public", kwargs={'barber_id': self.barber2.id})
        self.barber_1_serv_url = reverse("get_barber_services_public", kwargs={'barber_id': self.barber1.id})
        self.barber_2_serv_url = reverse("get_barber_services_public", kwargs={'barber_id': self.barber2.id})

    def test_get_barbers_list_success(self):
        """
        Return a list of all active barbers to unauthenticated users; excludes inactive.
        """
        resp = self.client.get(self.barber_list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Only barber1/barber2 present
        ids = [b["id"] for b in resp.data["barbers"]]
        self.assertIn(self.barber1.id, ids)
        self.assertIn(self.barber2.id, ids)
        self.assertNotIn(self.barber_inactive.id, ids)
        # Correct content fields
        for b in resp.data["barbers"]:
            self.assertIn("id", b)
            self.assertIn("username", b)
            self.assertIn("name", b)
            self.assertIn("surname", b)
            self.assertIn("description", b)

    def test_get_barber_profile_public_success(self):
        """
        Can get public profile for a barber, including their services and reviews.
        """
        resp = self.client.get(self.barber_1_profile_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Includes barber id, username, name, services and reviews
        self.assertEqual(resp.data["id"], self.barber1.id)
        self.assertEqual(resp.data["username"], self.barber1.username)
        self.assertIn("services", resp.data)
        self.assertIn("reviews", resp.data)
        # Services and reviews should have at least one item each
        self.assertTrue(any(service["id"] == self.service1.id for service in resp.data["services"]))
        self.assertTrue(any(review["id"] == self.review.id for review in resp.data["reviews"]))
        self.assertIn("name", resp.data)
        self.assertIn("surname", resp.data)

    def test_get_barber_profile_not_found(self):
        """
        Request a non-existent or inactive barber's profile returns error.
        """
        url = reverse("get_barber_profile_public", kwargs={"barber_id": 99999})
        resp = self.client.get(url)
        # Should be 400 because serializer raises ValidationError, not 404
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp.data["detail"]).lower())

        url = reverse("get_barber_profile_public", kwargs={"barber_id": self.barber_inactive.id})
        resp2 = self.client.get(url)
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp2.data["detail"]).lower())

    def test_get_barber_availabilities_public_success(self):
        """
        Can fetch all availabilities for a barber (public).
        """
        response = self.client.get(self.barber_1_avail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should show both availabilities for this barber
        list_out = response.data["availability"]
        self.assertTrue(any(a["slots"] == ["09:00", "10:00"] for a in list_out))
        self.assertTrue(any(a["date"] == self.tomorrow for a in list_out))

    def test_get_barber_availabilities_not_found(self):
        """
        Error if barber doesn't exist or inactive for public availabilities.
        """
        url = reverse("get_barber_availabilities_public", kwargs={"barber_id": 99999})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp.data["detail"]).lower())

        url = reverse("get_barber_availabilities_public", kwargs={"barber_id": self.barber_inactive.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp.data["detail"]).lower())

    def test_get_barber_services_public_success(self):
        """
        Can fetch all services for a barber (public).
        """
        resp = self.client.get(self.barber_1_serv_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Should return Fade and Lineup for barber1
        ids = [s["id"] for s in resp.data["services"]]
        self.assertIn(self.service1.id, ids)
        self.assertIn(self.service2.id, ids)
        # Should not include services from other barbers
        self.assertNotIn(self.service3.id, ids)

    def test_get_barber_services_public_not_found(self):
        """
        Error if barber doesn't exist or inactive when fetching services.
        """
        url = reverse("get_barber_services_public", kwargs={"barber_id": 9123782})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp.data["detail"]).lower())

        url = reverse("get_barber_services_public", kwargs={"barber_id": self.barber_inactive.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(resp.data["detail"]).lower())

    def test_public_routes_are_unauthenticated(self):
        """
        All public barber endpoints should allow access without authentication.
        """
        # (No special login needed for these endpoints)
        resp = self.client.get(self.barber_list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.get(self.barber_1_profile_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.get(self.barber_2_avail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.get(self.barber_2_serv_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_barbers_list_returns_empty_if_no_active_barbers(self):
        """
        Returns empty list if no barbers are active.
        """
        Barber.objects.all().delete()
        resp = self.client.get(self.barber_list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["barbers"], [])

    def test_inactive_barbers_are_not_returned_anywhere(self):
        """
        Inactive barbers should not be returned by any endpoint.
        """
        # None of the endpoints should expose data for self.barber_inactive
        # (already checked by specific tests, but verifies via all endpoints)
        user_endpoints = [
            reverse("get_barber_profile_public", kwargs={"barber_id": self.barber_inactive.id}),
            reverse("get_barber_availabilities_public", kwargs={"barber_id": self.barber_inactive.id}),
            reverse("get_barber_services_public", kwargs={"barber_id": self.barber_inactive.id}),
        ]
        for url in user_endpoints:
            resp = self.client.get(url)
            self.assertNotEqual(resp.status_code, status.HTTP_200_OK)  # Return 400
            self.assertIn("does not exist", str(resp.data["detail"]).lower())
