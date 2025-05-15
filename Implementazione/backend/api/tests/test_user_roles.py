from django.test import TestCase
from api.models import User, Roles

class UserRoleTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="adminpass",
            role=Roles.ADMIN.value
        )
        self.client_user = User.objects.create_user(
            username="clientuser",
            email="client@example.com",
            password="clientpass",
            role=Roles.CLIENT.value
        )
        self.barber = User.objects.create_user(
            username="barberuser",
            email="barber@example.com",
            password="barberpass",
            role=Roles.BARBER.value
        )

    def test_admin_role(self):
        self.assertEqual(self.admin.role, Roles.ADMIN.value)
        self.assertTrue(self.admin.is_admin())
        self.assertFalse(self.admin.is_client())
        self.assertFalse(self.admin.is_barber())

    def test_client_role(self):
        self.assertEqual(self.client_user.role, Roles.CLIENT.value)
        self.assertTrue(self.client_user.is_client())
        self.assertFalse(self.client_user.is_admin())
        self.assertFalse(self.client_user.is_barber())

    def test_barber_role(self):
        self.assertEqual(self.barber.role, Roles.BARBER.value)
        self.assertTrue(self.barber.is_barber())
        self.assertFalse(self.barber.is_admin())
        self.assertFalse(self.barber.is_client())
