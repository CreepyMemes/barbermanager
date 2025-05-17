from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
import re
from api.models import User



class PasswordResetTest(APITestCase):
    """
    Tests for password reset request and confirmation endpoints.
    """
    def setUp(self):
        self.reset_request_url = reverse('request_password_reset')
        self.reset_confirm_url_name = 'confirm_password_reset'

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


    def test_request_password_reset_sends_email(self):
        """
        Request password reset with valid email sends an email.
        """
        response = self.client.post(self.reset_request_url, {'email': self.user_email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)

        # Extract uid and token from the verification email
        match = re.search(r'/api/auth/reset-password/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/', mail.outbox[0].body)
        self.assertIsNotNone(match, "Registration link not found in email body")


    def test_request_password_reset_no_email_provided(self):
        """
        Request password reset with no email returns error.
        """
        response = self.client.post(self.reset_request_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('email'), ['This field is required.'])


    def test_request_password_reset_nonexistent_email(self):
        """
        Request password reset with non-existent email succeeds silently without email sent.
        """
        response = self.client.post(self.reset_request_url, {'email': 'nonexistent@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)
        self.assertEqual(len(mail.outbox), 0)


    def test_confirm_password_reset_success(self):
        """
        Confirm password reset with valid uid and token successfully resets password.
        """
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        new_password = 'NewStrongPassw0rd!'

        url = reverse(self.reset_confirm_url_name, kwargs={'uidb64': uidb64, 'token': token})
        response = self.client.post(url, {'password': new_password}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Password has been reset successfully.')

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))


    def test_confirm_password_reset_no_password(self):
        """
        Confirm password reset without providing password returns error.
        """
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        url = reverse(self.reset_confirm_url_name, kwargs={'uidb64': uidb64, 'token': token})
        response = self.client.post(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('password'), ['This field is required.'])


    def test_confirm_password_reset_invalid_uid(self):
        """
        Confirm password reset with invalid uid returns error.
        """
        token = default_token_generator.make_token(self.user)

        url = reverse(self.reset_confirm_url_name, kwargs={'uidb64': 'invaliduid', 'token': token})
        response = self.client.post(url, {'password': 'SomePass123!'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Invalid reset link.')


    def test_confirm_password_reset_invalid_token(self):
        """
        Confirm password reset with invalid token returns error.
        """
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))

        url = reverse(self.reset_confirm_url_name, kwargs={'uidb64': uidb64, 'token': 'invalidtoken'})
        response = self.client.post(url, {'password': 'SomePass123!'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Invalid or expired token')


    def test_confirm_password_reset_invalid_password(self):
        """
        Confirm password reset with invalid password returns validation error.
        """
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        url = reverse(self.reset_confirm_url_name, kwargs={'uidb64': uidb64, 'token': token})
        response = self.client.post(url, {'password': '123'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
