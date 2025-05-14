from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom utente object for unique email
class Utente(AbstractUser):
    email = models.EmailField(unique=True)