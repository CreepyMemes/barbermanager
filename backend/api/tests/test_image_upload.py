import os
import shutil
import tempfile
from PIL import Image
from django.conf import settings
from django.test import override_settings

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import (
    Admin,
    Barber,
    Client,
)

# Set up a temporary MEDIA_ROOT for the class
TEMP_MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ImageUploadTest(APITestCase):
    """
    Tests for the client profile management and appointment/review endpoints.
    """
    
    def setUp(self):
        # Endpoint URLs
        self.login_url = reverse("login_user")
        self.manage_image_url = reverse("manage_profile_image")
        self.profile_url_map = {
            'admin': reverse("get_admin_profile"),
            'barber': reverse("manage_barber_profile"),
            'client': reverse("manage_client_profile"),
        }

        # Create Users
        self.admin_password = "AdminSTRONG!"
        self.admin_user = Admin.objects.create_superuser(
            username="adminis123",
            password=self.admin_password,
        )

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


    @classmethod
    def tearDownClass(cls):
        # Remove the entire temp media directory after all tests
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    def login_as(self, user_type):
        creds = {
            "admin": (self.admin_user.username, self.admin_password),
            "barber": (self.barber_user.username, self.barber_password),
            "client": (self.client_user.username, self.client_password),
        }
        username, password = creds[user_type]
        response = self.client.post(self.login_url, {"username": username, "password": password}, format="json")
        token = response.data["token"]["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


    def create_temp_image(self, ext='jpeg', size=(10, 10), color=(123, 123, 123)):
        """
        Creates an in-memory image file ready to upload
        """
        temp_image = tempfile.NamedTemporaryFile(suffix=f'.{ext}')
        img = Image.new('RGB', size, color)
        img.save(temp_image, format=ext.upper())
        temp_image.seek(0)
        return temp_image
    

    def get_image_path(self, profile_image_url):
        """
        Given the profile image url (e.g. /media/images/profile/abc.jpg), return absolute file path.
        """
        relative_path = profile_image_url.replace('/media/', '')
        return os.path.join(TEMP_MEDIA_ROOT, relative_path) # Use TEMP_MEDIA_ROOT due to overriden settings
    

    def upload_profile_image(self, user_type):
        """
        Uploads image for given user type and returns (response, absolute file path)
        """
        self.login_as(user_type)

        # Attempt to upload a profile image as authenticated user
        payload = {'profile_image': self.create_temp_image()}
        response = self.client.post(self.manage_image_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Retrieve profile and check image URL, file presence
        response = self.client.get(self.profile_url_map[user_type])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile = response.data["profile"]
        file_path = self.get_image_path(profile['profile_image'])
        self.assertTrue(os.path.exists(file_path))

        return profile, file_path
    

    def delete_profile_image(self, user_type):
        """
        Uploads then deletes profile image for given user type, asserts removal.
        """
        profile, file_path = self.upload_profile_image(user_type)

        # Now delete
        response = self.client.delete(self.manage_image_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Refresh profile - may need to log in again if backend changes state
        response = self.client.get(self.profile_url_map[user_type])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile = response.data['profile']

        # After delete, field should be empty or None, file gone
        self.assertEqual(profile['profile_image'], None)
        self.assertFalse(os.path.exists(file_path))


    def test_upload_profile_image_success(self):
        """
        Users can upload and retrieve their own profile image url.
        """
        self.upload_profile_image('admin')
        self.upload_profile_image('barber')
        self.upload_profile_image('client')


    def test_delete_profile_image_success(self):
        """
        Users can upload and then delete their profile image.
        """
        self.delete_profile_image('admin')
        self.delete_profile_image('barber')
        self.delete_profile_image('client')


    def test_upload_profile_image_bad_request(self):
        """
        Users can't upload a non-image.
        """
        self.login_as("admin")
        with tempfile.NamedTemporaryFile(suffix='.txt') as fake_file:
            fake_file.write(b'not an image')
            fake_file.seek(0)
            payload = {'profile_image': fake_file}
            resp = self.client.post(self.manage_image_url, payload, format='multipart')
            self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


    def test_upload_requires_auth(self):
        """
        Uploading a profile image without authentication is rejected.
        """
        # Do not log in
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'profile_image': image_file}
            response = self.client.post(self.manage_image_url, payload, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_delete_requires_auth(self):
        """
        Deleting a profile image without authentication is rejected.
        """
        response = self.client.delete(self.manage_image_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)