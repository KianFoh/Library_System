"""
Django settings for library_system_backend project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os 
import pytz
from celery.schedules import crontab, schedule

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&agse^&mcl+e_-u$0*rdv3ye-f66c$odu-sur_st#6y9+3t$0('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

SITE_ID = 1 

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Own
    'navigation.apps.NavigationConfig',
    'home.apps.HomeConfig',
    'rooms.apps.RoomsConfig',
    'bookings.apps.BookingsConfig',
    'contact.apps.ContactConfig',
    'footer.apps.FooterConfig',
    'authentication.apps.AuthenticationConfig',
    'profile_.apps.ProfileConfig',
    'user_data.apps.UserDataConfig',
    'crispy_forms',
    'crispy_bootstrap4',
    'pytz',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_celery_beat',
]
SOCIALACCOUNT_LOGIN_ON_GET= True
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE":[
            "profile",
            "email"
        ],
        "AUTH_PARAMS": {"access_type": "online"}
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware", # remove this, which only used in v0.56+
    'authentication.middleware.RestrictAllauthAccessMiddleware',
]

ROOT_URLCONF = 'library_system_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'library_system_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '123tkf',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Set the timezone to Malaysia time
TIME_ZONE = 'Asia/Kuala_Lumpur'

# Enable timezone support
USE_TZ = False
USE_I18N = True

# Set the date format to DD/MM/YYYY
DATE_FORMAT = 'd/m/Y'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Emailing settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'intilibrarysystem@gmail.com'
EMAIL_HOST_PASSWORD = 'nymm eepy zoct uxeq'

# Email Verification Expire time
PASSWORD_RESET_TIMEOUT = 10000

# Media saving location
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Google sign in 
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_ADAPTER = 'authentication.adapter.MySocialAccountAdapter'

# Celery Configuration


CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'rpc://'  # Using RPC as the result backend

CELERY_BEAT_SCHEDULE = {
    'reset_timeslot': {
        'task': 'bookings.tasks.reset_timeslots_status',
        'schedule': crontab(hour=8, minute=0),  # Run every day at 8 AM
    },
    'reset_room_usage_hour_task': {
        'task': 'bookings.tasks.reset_room_usage_hour',
        'schedule': crontab(hour=8, minute=0),  # Run every day at 8 AM
    },
}

