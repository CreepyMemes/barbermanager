from django.contrib.auth import get_user_model


User = get_user_model()


def generate_unique_username(email):
    """
    Generates a unique username based on the email prefix.
    If username exists, appends an incrementing suffix.
    """
    base = email.split('@')[0]
    username = base
    count = 1

    while User.objects.filter(username=username).exists():
        username = f"{base}_{count}"
        count += 1

    return username