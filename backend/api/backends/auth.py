from django.contrib.auth.backends import ModelBackend


class UsernameOrEmailBackend(ModelBackend):
    """
    Custom authentication backend to allow login with either username or email.
    Gives precedence to username (especially for admins with no email).
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        from ..models import User
        
        if not username or not password:
            return None
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        
        return None