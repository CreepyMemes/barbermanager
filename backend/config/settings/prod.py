from .base import *

DEBUG = False
FRONTEND_URL = os.environ['FRONTEND_URL']
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)
SECURE_HSTS_SECONDS = 31536000  # 1 year, match your nginx max-age
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True