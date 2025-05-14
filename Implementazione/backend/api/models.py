from django.contrib.auth.models import AbstractUser
from django.db import models

# Make email unique
class Utente(AbstractUser):
    email = models.EmailField(unique=True)