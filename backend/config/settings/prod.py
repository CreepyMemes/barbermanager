from .base import *

DEBUG = False
FRONTEND_URL = os.environ['FRONTEND_URL']
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)