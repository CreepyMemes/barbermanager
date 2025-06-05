# from rest_framework.test import APITestCase
# from django.urls import reverse
# from rest_framework import status
# from api.models.user import User, UserRole
# from api.models.appointment import Appointment, AppointmentStatus

# class ClientAppointmentsTest(APITestCase):

#     def setUp(self):
#         self.client_user = User.objects.create_user(
#             email="client@example.com", password="pass1234", role=UserRole.CLIENT
#         )
#         self.client.login(email="client@example.com", password="pass1234")

#     def test_list_past_appointments(self):
#         Appointment.objects.create(
#             client=self.client_user,
#             status=AppointmentStatus.COMPLETED,
#             date="2024-06-01",
#             slot="10:00"
#         )
#         url = reverse('client-appointments-list')  # Aggiungi name alla url
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertGreaterEqual(len(response.data), 1)
