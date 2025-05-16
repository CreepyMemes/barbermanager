from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from enum import Enum

class Roles(Enum):
    """
    User role definitions: Admin, Client, Barber.
    """
    ADMIN = "ADMIN"
    CLIENT = "CLIENT"
    BARBER = "BARBER"

    @classmethod
    def choices(cls):
        return [(role.value, role.name) for role in cls]


class UserManager(BaseUserManager):
    """
    Custom user manager to handle user and superuser creation.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        extra_fields.setdefault('role', Roles.CLIENT.value)

        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', Roles.ADMIN.value)

        user = self.create_user(email, password, **extra_fields)
        
        return user


class User(AbstractUser):
    """
    Custom user model using our custom manager.
    """
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Roles.choices(), default=Roles.CLIENT.value)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def is_client(self):
        return self.role == Roles.CLIENT.value

    def is_barber(self):
        return self.role == Roles.BARBER.value

    def is_admin(self):
        return self.role == Roles.ADMIN.value


class BarberInvitation(models.Model):
    """
    Keeps track of which barbers have been invited to register.
    """
    email = models.EmailField(unique=True)
    used = models.BooleanField(default=False)
    invited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email