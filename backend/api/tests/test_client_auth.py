from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from django.urls import reverse
from django.core import mail
from django.conf import settings
import re
from api.models import User, Client

@patch('django.core.mail.send_mail', return_value=1) 
class ClientAuthFlowTest(APITestCase):
    """
    Tests for full user registration, email verification, login, and logout flows.
    """
    def setUp(self):
        self.register_url = reverse('register_client')
        self.verify_url = 'verify_client_email'
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')

        # User data for tests
        self.user_email = 'resetuser@example.com'
        self.user_password = 'StrongPassw0rd!'
        self.user_username = 'resetuser'
        self.user_name = 'Name Test'
        self.user_surname = 'Surname Test'

        # Create an active user (used only if needed)
        self.client_user = Client.objects.create_user(
            username=self.user_username,
            email=self.user_email,
            password=self.user_password,
            name=self.user_name,
            surname=self.user_surname,
            is_active=True
        )


    def register_and_get_verification_link(self, email='testclient@example.com', username='testclient', password='StrongPassw0rd!', name='test name', surname='test surname'):
        """
        Helper to register a user and extract the verification link uid and token from the email.
        """
        data = {'email': email, 'password': password, 'username': username, 'name': name, 'surname': surname}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)

        # Verify user is created but inactive
        user = User.objects.get(email=email)
        self.assertFalse(user.is_active)

        # Look for a link of the form: FRONTEND_URL/verify/UID/TOKEN
        match = re.search(re.escape(settings.FRONTEND_URL) + r'/verify/(?P<uidb64>[^/]+)/(?P<token>[^/\s]+)', mail.outbox[0].body)
        self.assertIsNotNone(match, "Verification link not found in email body")

        return user, match.group('uidb64'), match.group('token')


    def test_full_registration_verification_login_logout_flow(self, mock_send_mail):
        """
        Full flow: register -> verify email -> login (username/email) -> logout.
        """
        user, uidb64, token = self.register_and_get_verification_link()

        # Verify email
        verify_url = reverse(self.verify_url, kwargs={'uidb64': uidb64, 'token': token})

        verify_response = self.client.get(verify_url)

        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', verify_response.data)
        self.assertEqual(verify_response.data.get('detail'), 'Email verified successfully.')

        # User should now be active
        user.refresh_from_db()
        self.assertTrue(user.is_active)

        # Login with username
        login_data = {'username': user.username, 'password': self.user_password}
        login_response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('token', login_response.data)
        access_token = login_response.data.get('token')['access_token']
        refresh_token = login_response.data.get('token')['refresh_token']

        # Login with email
        login_data_email = {'email': user.email, 'password': self.user_password}
        login_response_email = self.client.post(self.login_url, login_data_email, format='json')
        self.assertEqual(login_response_email.status_code, status.HTTP_200_OK)
        self.assertIn('token', login_response_email.data)

        # Logout
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        logout_response = self.client.post(self.logout_url, {'refresh_token': refresh_token}, format='json')
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertEqual(logout_response.data.get('detail'), 'Logout successful.')


    def test_verify_with_invalid_link(self, mock_send_mail):
        """
        Verify email with invalid uid/token returns error.
        """
        url = reverse(self.verify_url, kwargs={'uidb64': 'invalid-uid', 'token': 'wrong-token'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Invalid link.')


    def test_verify_with_expired_or_wrong_token(self, mock_send_mail):
        """
        Verify email with expired or wrong token returns error.
        """
        user, uidb64, token = self.register_and_get_verification_link()
        url = reverse(self.verify_url, kwargs={'uidb64': uidb64, 'token': 'wrong-token'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Invalid or expired token.')


    def test_login_fails_with_unverified_account(self, mock_send_mail):
        """
        Login fails if account is inactive (email not verified).
        """
        user, _, _ = self.register_and_get_verification_link(email='unverified@example.com', username='unverified')
        login_data = {'email': user.email, 'password': self.user_password}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'Account inactive. Please verify your email.')


    def test_login_fails_with_wrong_credentials(self, mock_send_mail):
        """
        Login fails with incorrect password.
        """
        user, uidb64, token = self.register_and_get_verification_link(email='wrongcred@example.com', username='wrongcred')
        verify_url = reverse(self.verify_url, kwargs={'uidb64': uidb64, 'token': token})
        self.client.get(verify_url)
        user.refresh_from_db()

        login_data = {'email': user.email, 'password': 'WrongPass!'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'Invalid credentials.')


    def test_logout_fails_without_refresh_token(self, mock_send_mail):
        """
        Logout fails if refresh token not provided.
        """
        user, uidb64, token = self.register_and_get_verification_link(email='logoutfail@example.com', username='logoutfail')
        verify_url = reverse(self.verify_url, kwargs={'uidb64': uidb64, 'token': token})
        self.client.get(verify_url)
        user.refresh_from_db()

        login_data = {'email': user.email, 'password': self.user_password}
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data.get('token')['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.logout_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('refresh_token')[0], 'This field is required.')


    def test_logout_fails_with_invalid_refresh_token(self, mock_send_mail):
        """
        Logout fails with invalid refresh token.
        """
        user, uidb64, token = self.register_and_get_verification_link(email='logoutinvalid@example.com', username='logoutinvalid')
        verify_url = reverse(self.verify_url, kwargs={'uidb64': uidb64, 'token': token})
        self.client.get(verify_url)
        user.refresh_from_db()

        login_data = {'email': user.email, 'password': self.user_password}
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data.get('token')['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.logout_url, {'refresh_token': 'invalid-token'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('refresh_token')[0], 'Invalid or expired refresh token.')


    def test_registration_fails_with_invalid_username(self, mock_send_mail):
        """
        Registration should fail if username contains illegal characters (e.g., spaces).
        """
        data = { 'email': 'badusername@example.com', 'password': 'StrongPassw0rd!', 'username': 'invalid user', 'name': 'Name', 'surname': 'Surname'}

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("Username can only contain ASCII letters, digits, and underscores", response.data['detail'])

    
    def test_registration_fails_with_invalid_phone_number(self, mock_send_mail):
        """
        Registration should fail if phone number is not in E.164 format.
        """
        data = { 'email': 'badphone@example.com', 'password': 'StrongPassw0rd!', 'username': 'badphoneuser', 'name': 'Name', 'surname': 'Surname', 'phone_number': '1234-notaphone'}
        
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed (E.164 format).", response.data['detail'])