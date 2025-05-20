from .base import *

DEBUG = False
FRONTEND_URL = 'http://barbermanager.creepymemes.duckdns.org'
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)