from .base import *

DEBUG = False
FRONTEND_URL = 'http://manageBarber.s1lentCommit.org'
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)