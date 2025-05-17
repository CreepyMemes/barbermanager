from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core import mail
import re
from api.models import User


class AuthFlowTest(APITestCase):
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

        # Create an active user (used only if needed)
        self.user = User.objects.create_user(
            username=self.user_username,
            email=self.user_email,
            password=self.user_password,
            is_active=True
        )


    def register_and_get_verification_link(self, email='testclient@example.com', username='testclient', password='StrongPassw0rd!'):
        """
        Helper to register a user and extract the verification link uid and token from the email.
        """
        data = {'email': email, 'password': password, 'username': username}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)

        # Verify user is created but inactive
        user = User.objects.get(email=email)
        self.assertFalse(user.is_active)

        # Extract uid and token from the verification email
        match = re.search(r'/api/auth/verify/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/', mail.outbox[0].body)
        self.assertIsNotNone(match, "Verification link not found in email body")
        return user, match.group('uidb64'), match.group('token')


    def test_full_registration_verification_login_logout_flow(self):
        """
        Full flow: register -> verify email -> login (username/email) -> logout.
        """
        user, uidb64, token = self.register_and_get_verification_link()

        # Verify email
        verify_url = reverse(self.verify_url, kwargs={'uidb64': uidb64, 'token': token})
        verify_response = self.client.get(verify_url)
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', verify_response.data)
        self.assertEqual(verify_response.data['detail'], 'Email verified successfully.')

        # User should now be active
        user.refresh_from_db()
        self.assertTrue(user.is_active)

        # Login with username
        login_data = {'username': user.username, 'password': self.user_password}
        login_response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('token', login_response.data)
        access_token = login_response.data['token']['access_token']
        refresh_token = login_response.data['token']['refresh_token']

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


    def test_verify_with_invalid_link(self):
        """
        Verify email with invalid uid/token returns error.
        """
        url = reverse(self.verify_url, kwargs={'uidb64': 'invalid-uid', 'token': 'wrong-token'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Invalid verification link.')


    def test_verify_with_expired_or_wrong_token(self):
        """
        Verify email with expired or wrong token returns error.
        """
        user, uidb64, token = self.register_and_get_verification_link()
        url = reverse(self.verify_url, kwargs={'uidb64': uidb64, 'token': 'wrong-token'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Invalid or expired token.')


    def test_login_fails_with_unverified_account(self):
        """
        Login fails if account is inactive (email not verified).
        """
        user, _, _ = self.register_and_get_verification_link(email='unverified@example.com', username='unverified')
        login_data = {'email': user.email, 'password': self.user_password}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'Account inactive. Please verify your email.')


    def test_login_fails_with_wrong_credentials(self):
        """
        Login fails with incorrect password.
        """
        user, uidb64, token = self.register_and_get_verification_link(email='wrongcred@example.com', username='wrongcred')
        verify_url = reverse(self.verify_url, kwargs={'uidb64': uidb64, 'token': token})
        self.client.get(verify_url)
        user.refresh_from_db()

        login_data = {'email': user.email, 'password': 'WrongPass!'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Invalid credentials')


    def test_logout_fails_without_refresh_token(self):
        """
        Logout fails if refresh token not provided.
        """
        user, uidb64, token = self.register_and_get_verification_link(email='logoutfail@example.com', username='logoutfail')
        verify_url = reverse(self.verify_url, kwargs={'uidb64': uidb64, 'token': token})
        self.client.get(verify_url)
        user.refresh_from_db()

        login_data = {'email': user.email, 'password': self.user_password}
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data['token']['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.logout_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('refresh_token'), 'Refresh token is required.')


    def test_logout_fails_with_invalid_refresh_token(self):
        """
        Logout fails with invalid refresh token.
        """
        user, uidb64, token = self.register_and_get_verification_link(email='logoutinvalid@example.com', username='logoutinvalid')
        verify_url = reverse(self.verify_url, kwargs={'uidb64': uidb64, 'token': token})
        self.client.get(verify_url)
        user.refresh_from_db()

        login_data = {'email': user.email, 'password': self.user_password}
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data['token']['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.logout_url, {'refresh_token': 'invalid-token'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Invalid token or token already blacklisted.')