import os

from .common import *  # NOQA F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '3306',
    }
}

APP_NAME = "MoneyBook"

ALLOWED_HOSTS = [os.environ.get('HOST_NAME')]

# CSRF protection for HTTPS
# Django 4.0+ requires CSRF_TRUSTED_ORIGINS for cross-origin requests over HTTPS
# Construct from HOST_NAME with https:// scheme
_host_name = os.environ.get('HOST_NAME')
CSRF_TRUSTED_ORIGINS = [f'https://{_host_name}']

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')
