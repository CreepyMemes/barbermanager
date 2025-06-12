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
        'ENGINE': os.getenv('SQL_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ['SQL_DATABASE'],
        'USER': os.environ['SQL_USER'],
        'PASSWORD': os.environ['SQL_PASSWORD'],
        'HOST': os.getenv('SQL_HOST', 'localhost'),
        'PORT': os.getenv('SQL_PORT', '5432'),
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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django's email service settings
EMAIL_BACKEND = os.environ['EMAIL_BACKEND']
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = int(os.environ['EMAIL_PORT'])
EMAIL_USE_TLS = bool(int(os.environ['EMAIL_USE_TLS']))
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER'] 
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD'] 

# Celery tasks settings
CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL'] 
CELERY_RESULT_BACKEND =os.environ['CELERY_RESULT_BACKEND'] 
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULE = {
    'complete-ongoing-appointments': {
        'task': 'api.tasks.complete_ongoing_appointments',
        'schedule': crontab(minute='*/1'),
    },
}

# WARNING: this is only for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True