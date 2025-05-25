from .base import *

DEBUG = False
FRONTEND_URL = os.environ['FRONTEND_URL']
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Set HSTS on every subdomain
SECURE_HSTS_SECONDS = 31536000         # Match nginx config
SECURE_SSL_REDIRECT = False            # No need as nginx redirects