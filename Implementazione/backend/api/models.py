from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum

class Roles(Enum):
    ADMIN = "ADMIN"
    CLIENT = "CLIENT"
    BARBER = "BARBER"

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name) for tag in cls]

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=Roles.choices(), default=Roles.CLIENT.value)

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def is_client(self):
        return self.role == Roles.CLIENT.value

    def is_barber(self):
        return self.role == Roles.BARBER.value

    def is_admin(self):
        return self.role == Roles.ADMIN.value
