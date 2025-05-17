from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import Q, UniqueConstraint
from django.db import models
from enum import Enum


class Roles(Enum):
    """
    User role definitions: Admin, Client, Barber.
    """
    ADMIN = 'ADMIN'
    CLIENT = 'CLIENT'
    BARBER = 'BARBER'

    @classmethod
    def choices(cls):
        return [(role.value, role.name) for role in cls]


class UserManager(BaseUserManager):
    """
    Custom user manager to handle user and superuser creation.
    """
    def create_user(self, username, email=None, password=None, **extra_fields):
        
        if not username:
            raise ValueError('Username is required')
        
        role = extra_fields.get('role', Roles.CLIENT.value)

        if role != Roles.ADMIN.value and not email:
            raise ValueError('Email is required for non-admin users')

        if email:
            email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', Roles.ADMIN.value)

        if not username:
            raise ValueError('Superuser must have a username')
        
        if extra_fields.get('role') != Roles.ADMIN.value:
            raise ValueError('Superuser must have role=ADMIN')
        
        user = self.create_user(username=username, email=None, password=password, **extra_fields)
        
        return user


class User(AbstractUser):
    """
    Custom user model using our custom manager.
    """
    email = models.EmailField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=Roles.choices(), default=Roles.CLIENT.value)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['email'],
                condition=~Q(role=Roles.ADMIN.value),  # only enforce uniqueness for non-admins
                name='unique_email_non_admin'
            )
        ]

    def get_role(self):
        return self.role


class Client(User):
    """
    Clients are regular users who can register themselves via the API.
    They must provide a valid email and username during registration.
    """
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = Roles.CLIENT.value

        if not self.email:
            raise ValueError('Client must have an email')
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Barber(User):
    """
    Barbers can only register if invited by an admin. They register by 
    providing a username and password, email is set by admin invitation.
    """
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = Roles.BARBER.value

        if not self.email:
            raise ValueError('Barber must have an email')
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Barber'
        verbose_name_plural = 'Barbers'


class Admin(User):
    """
    Admins are created by the system using the `createsuperuser` command.
    They are granted full permissions (staff and superuser) and do not require an email.
    """
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = Roles.ADMIN.value

        self.is_staff = True
        self.is_superuser = True

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
    