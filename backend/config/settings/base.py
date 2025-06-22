import os
from pathlib import Path
from datetime import timedelta
from celery.schedules import crontab

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Django's secret key
SECRET_KEY = os.environ['SECRET_KEY']

# Allowed host ips
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split()

# Defined installed apps in use
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'api',
]

# idk what this means
SITE_ID = 1

# Custom authentication backend for logging with either email/pass or usrname/pass
AUTHENTICATION_BACKENDS = [
    'api.utils.UsernameOrEmailBackend', 
    'django.contrib.auth.backends.ModelBackend',
]

# Custom user model to be used
AUTH_USER_MODEL = 'api.User'

# Setting up default authentication to JWT token
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    'EXCEPTION_HANDLER': 'api.utils.customExceptionHandler',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Setting up JWT token lifetime
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Setting up django's hooks
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root url config path
ROOT_URLCONF = 'config.urls'

# I'm not sure if i need this as it's API only backend
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Development server location
WSGI_APPLICATION = 'config.wsgi.application'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT'],
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = "Europe/Rome"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# User uploaded media dirs
MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django's email service settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER'] 
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD'] 

# Celery tasks settings
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_WORKER_STATE_DB = '/tmp/celeryworker.state'
CELERY_BEAT_SCHEDULE_FILENAME = '/tmp/celerybeat.schedule'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = "Europe/Rome"
CELERY_BEAT_SCHEDULE = {
    'complete-ongoing-appointments': {
        'task': 'api.tasks.complete_ongoing_appointments',
        'schedule': crontab(minute='*/1'),
    },
    'send-appointment-reminders': {
        'task': 'api.tasks.send_appointment_reminders',
        'schedule': crontab(minute='*/1'),
    },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Barber Manager API",
    "DESCRIPTION": "Manage barbershop scheduling, reviews, and users.",
    "VERSION": "1.0.0",
    "SWAGGER_UI_SETTINGS": '''{
        deepLinking: true,
        urls: [
            {url: "/api/schema/", name: "v1"},
        ],
        presets: [SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset],
        layout: "StandaloneLayout",
    }''',

    "SERVERS": [{"url": "/api"}],
    # "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX_TRIM": "/api",
    'COMPONENT_SPLIT_REQUEST': True,
}

# WARNING: this is only for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True