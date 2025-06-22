import os
import uuid
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import  force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from rest_framework import serializers


phone_number_validator = RegexValidator(
    regex=r'^\+?[1-9]\d{1,14}$', 
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed (E.164 format)."
)


def get_profile_image_path(instance, filename):
    """
    Utility function that generates a unique file path for the uploaded profile picture.
    Example: images/profile/1a2b3c4d5e6f7g8h9i0j.png
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('images', 'profile', filename)


def get_user_from_uid_token(uidb64, token, role=None):
    """
    Utility function that checks if a token previously registered to a user is valid.
    Raises serializers.ValidationError if invalid.
    """
    from ..models import User

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        if role:
            user = User.objects.get(pk=uid, role=role)
        else:
            user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise serializers.ValidationError("Invalid link.")
    
    if not default_token_generator.check_token(user, token):
        raise serializers.ValidationError("Invalid or expired token.")

    return user
