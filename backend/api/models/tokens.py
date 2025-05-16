from django.db import models
import uuid

class BarberInvitation(models.Model):
    """
    Keeps track of which barbers have been invited to register.
    """
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email