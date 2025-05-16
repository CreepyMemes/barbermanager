from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RefreshTokenTest(APITestCase):
    """
    Tests for the refresh_token endpoint.
    """
    def setUp(self):
        self.refresh_url = reverse('refresh_token')  # Ensure this name is registered in your urls.py
        self.user = User.objects.create_user(
            username='refreshtest',
            email='refreshtest@example.com',
            password='StrongPassw0rd!',
            is_active=True
        )
        self.refresh_token = str(RefreshToken.for_user(self.user))


    def test_refresh_token_success(self):
        """
        Successfully refreshes access token.
        """
        response = self.client.post(self.refresh_url, {'refresh_token': self.refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('expires_in', response.data)
        self.assertEqual(response.data['token_type'], 'Bearer')


    def test_refresh_token_missing(self):
        """
        Refresh fails when token is not provided.
        """
        response = self.client.post(self.refresh_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'), 'Refresh token is required.')


    def test_refresh_token_invalid(self):
        """
        Refresh fails with invalid token.
        """
        response = self.client.post(self.refresh_url, {'refresh_token': 'invalid.token.here'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
