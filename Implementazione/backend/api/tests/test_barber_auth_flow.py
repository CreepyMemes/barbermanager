from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core import mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from unittest.mock import patch
import uuid
from api.models import User, BarberInvitation, Roles
from api.serializers import BarberRegisterSerializer, BarberInviteSerializer


class BarberAuthFlowTest(APITestCase):
    """
    Tests for barber invitation and registration flows.
    """
    def setUp(self):
        self.invite_url = reverse('invite_barber')
        # register_barber URL will be generated dynamically as it requires uid and token

        # Create admin user to authenticate invite requests
        self.admin_username = 'root'
        self.admin_password = 'AdminPass123!'
        self.admin_user = User.objects.create_user(
            username=self.admin_username,
            email='root@test.com',
            password=self.admin_password,
            role=Roles.ADMIN.value,
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        self.barber_password = 'BarberPass123!'

    def authenticate_admin(self):
        login_url = reverse('login_user')
        response = self.client.post(login_url, {'username': self.admin_username, 'password': self.admin_password}, format='json')
        token = response.data['token']['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_invite_barber_success(self):
        """
        Admin can invite a barber successfully, and an invitation email is sent.
        """
        self.authenticate_admin()

        data = {'email': 'newbarber@example.com'}
        response = self.client.post(self.invite_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "Invitation sent.")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('newbarber@example.com', mail.outbox[0].to)
        # Confirm BarberInvitation created
        invitation = BarberInvitation.objects.filter(email=data['email'], used=False).first()
        self.assertIsNotNone(invitation)

    def test_invite_barber_already_exists(self):
        """
        Inviting a barber with an email that already belongs to a user returns 400.
        """
        self.authenticate_admin()

        existing_email = 'existingbarber@example.com'
        User.objects.create_user(
            username='existingbarber',
            email=existing_email,
            password='somepass',
            role=Roles.BARBER.value,
            is_active=True
        )

        response = self.client.post(self.invite_url, {'email': existing_email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "A user with this email already exists.")

    def test_invite_barber_already_invited(self):
        """
        Inviting a barber who already has a pending invitation returns 400.
        """
        self.authenticate_admin()

        email = 'pendingbarber@example.com'
        BarberInvitation.objects.create(email=email, used=False)

        response = self.client.post(self.invite_url, {'email': email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Invitation already sent to this email.")

    def test_register_barber_success(self):
        """
        A barber can register successfully using a valid uid and token.
        """
        # Prepare invitation
        email = 'registerbarber@example.com'
        invitation = BarberInvitation.objects.create(email=email, used=False)

        uid = urlsafe_base64_encode(force_bytes(email))
        token = str(invitation.token)
        register_url = reverse('register_barber', kwargs={'uidb64': uid, 'token': token})

        data = {'password': self.barber_password}
        response = self.client.post(register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Barber registered successfully.')

        # Check user created and active with correct role
        user = User.objects.filter(email=email).first()
        self.assertIsNotNone(user)
        self.assertTrue(user.is_active)
        self.assertEqual(user.role, Roles.BARBER.value)

        # Invitation should be marked used
        invitation.refresh_from_db()
        self.assertTrue(invitation.used)

    def test_register_barber_invalid_uid(self):
        """
        Registering with invalid UID returns error.
        """
        email = 'foo@example.com'
        invitation = BarberInvitation.objects.create(email=email, used=False)
        invalid_uid = 'invaliduid'
        token = str(invitation.token)

        register_url = reverse('register_barber', kwargs={'uidb64': invalid_uid, 'token': token})

        data = {'password': self.barber_password}
        response = self.client.post(register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid UID.')

    def test_register_barber_invalid_token(self):
        """
        Registering with a wrong token returns error.
        """
        email = 'barberwrongtoken@example.com'
        invitation = BarberInvitation.objects.create(email=email, used=False)
        uid = urlsafe_base64_encode(force_bytes(email))
        wrong_token = uuid.uuid4()  # Random token

        register_url = reverse('register_barber', kwargs={'uidb64': uid, 'token': wrong_token})

        data = {'password': self.barber_password}
        response = self.client.post(register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid invitation token.')

    def test_register_barber_already_registered(self):
        """
        Trying to register a barber who already exists returns error.
        """
        email = 'existingbarber2@example.com'
        invitation = BarberInvitation.objects.create(email=email, used=False)
        uid = urlsafe_base64_encode(force_bytes(email))
        token = str(invitation.token)

        User.objects.create_user(
            username='existingbarber2',
            email=email,
            password='somepass',
            role=Roles.BARBER.value,
            is_active=True
        )

        register_url = reverse('register_barber', kwargs={'uidb64': uid, 'token': token})
        data = {'password': self.barber_password}
        response = self.client.post(register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'User with this email already exists.')

