from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core import mail
import re
from api.models import User, Roles


class BarberAuthFlowTest(APITestCase):
    """
    Tests for barber invitation and registration flows.
    """
    def setUp(self):
        self.invite_url = reverse('invite_barber')
        self.login_url = reverse('login_user')
        self.register_url = 'register_barber'

        # User data for admin
        self.admin_username = 'root'
        self.admin_password = 'AdminPass123!'

        # Create admin user to authenticate invite requests
        self.admin = User.objects.create_user(
            username=self.admin_username,
            email=None,
            password=self.admin_password,
            role=Roles.ADMIN.value,
        )


    def authenticate_admin(self):
        """
        Helper to authenticate admin
        """
        response = self.client.post(self.login_url, {'username': self.admin_username, 'password': self.admin_password}, format='json')
        token = response.data.get('token')['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


    def invite_barber(self, email='newbarber@example.com'):
        """
        Helper to send invite as an admin, returns (response, uid, token)
        """
        self.authenticate_admin()

        data = {'email': email}
        response = self.client.post(self.invite_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('detail'), 'Barber invited successfully.')
    
        # Dynamically get the URL prefix without uid/token
        url_prefix = reverse(self.register_url, kwargs={'uidb64': 'UIDPLACEHOLDER', 'token': 'TOKENPLACEHOLDER'})

        # Build regex by replacing the placeholders with regex groups
        regex_pattern = url_prefix.replace('UIDPLACEHOLDER', r'(?P<uidb64>[^/]+)').replace('TOKENPLACEHOLDER', r'(?P<token>[^/]+)')

        # Search in the email body
        match = re.search(regex_pattern, mail.outbox[0].body)
        self.assertIsNotNone(match, "Verification link not found in email body")
    
        return response, match.group('uidb64'), match.group('token')
    

    def test_register_barber_success(self):
        """
        A barber can register successfully using a valid uid and token.
        """
        email = 'registerbarber@example.com'
        response, uid, token = self.invite_barber(email)

        self.assertEqual(response.data.get('detail'), 'Barber invited successfully.')
        
        register_url = reverse(self.register_url, kwargs={'uidb64': uid, 'token': token})

        data = {'username': 'newbarbertest', 'password': 'BarberPass123!', 'name': 'test name', 'surname': 'test surname', 'name': 'test name', 'surname': 'test surname'}
        response = self.client.post(register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('detail'), 'Barber registered and account activated.')

        # Check user created and active with correct role
        user = User.objects.filter(email=email).first()
        self.assertIsNotNone(user)
        self.assertTrue(user.is_active)
        self.assertEqual(user.role, Roles.BARBER.value)


    def test_register_barber_invalid_uid(self):
        """
        Registering with invalid UID returns error.
        """
        response, uid, token = self.invite_barber('invaliduid@example.com')

        self.assertEqual(response.data.get('detail'), 'Barber invited successfully.')
        
        register_url = reverse(self.register_url, kwargs={'uidb64': 'invalid-uid', 'token': token})

        data = {'username': 'newbarbertest', 'password': 'BarberPass123!', 'name': 'test name', 'surname': 'test surname'}
        response = self.client.post(register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Invalid link.')


    def test_register_barber_invalid_token(self):
        """
        Registering with invalid UID returns error.
        """
        response, uid, token = self.invite_barber('invalidtoken@example.com')

        self.assertEqual(response.data.get('detail'), 'Barber invited successfully.')
        
        register_url = reverse(self.register_url, kwargs={'uidb64': uid, 'token': 'invalid-token'})

        data = {'username': 'newbarbertest', 'password': 'BarberPass123!', 'name': 'test name', 'surname': 'test surname'}
        response = self.client.post(register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Invalid or expired token.')


    def test_invite_barber_already_regsitered(self):
        """
        Trying to register a barber who already exists returns error.
        """
        email = 'existingbarber@example.com'

        User.objects.create_user(
            username='existingbarber',
            email=email,
            password='somepass',
            role=Roles.BARBER.value,
            is_active=True
        )
        
        self.authenticate_admin()

        data = {'email': email}
        response = self.client.post(self.invite_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), f'The email "{email}" is already taken.')

