from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(
    regex=r'^\+?[1-9]\d{1,14}$', 
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed (E.164 format)."
)

username_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_]+$',
    message="Username may only contain ASCII letters, digits, and underscores (_).",
)
