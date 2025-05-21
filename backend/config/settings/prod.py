from .base import *

DEBUG = False
FRONTEND_URL = os.environ['APP_DOMAIN']
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)