from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from allauth.account.models import EmailAddress
from django.db import models
from enum import Enum

class Roles(Enum):
    """
    User role enum definition
    """
    ADMIN = "ADMIN"
    CLIENT = "CLIENT"
    BARBER = "BARBER"

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name) for tag in cls]


class UserManager(BaseUserManager):
    """
    Custom user manager definition for handling creation
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        extra_fields.setdefault('role', Roles.CLIENT.value)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Roles.ADMIN.value)

        user = self.create_user(email, password, **extra_fields)

        # Mark email as verified for allauth
        EmailAddress.objects.create(
            user=user,
            email=user.email,
            verified=True,
            primary=True,
        )
        return user


class User(AbstractUser):
    """
    Custom user model definition that uses the previous custom user manager
    """
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    role = models.CharField(max_length=10, choices=Roles.choices(), default=Roles.CLIENT.value)

    objects = UserManager()
    
    def is_client(self):
        return self.role == Roles.CLIENT.value

    def is_barber(self):
        return self.role == Roles.BARBER.value

    def is_admin(self):
        return self.role == Roles.ADMIN.value


class BarberInvitation(models.Model):
    """
    Store invited barber emails
    """
    email = models.EmailField(unique=True)
    used = models.BooleanField(default=False)
    invited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email