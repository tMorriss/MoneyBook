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

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

# CSRF protection for HTTPS
# Django 4.0+ requires CSRF_TRUSTED_ORIGINS for cross-origin requests over HTTPS
# Construct from ALLOWED_HOSTS with https:// scheme
_allowed_host = os.environ.get('ALLOWED_HOSTS', 'moneybook.tmorriss.com')
CSRF_TRUSTED_ORIGINS = [f'https://{_allowed_host}']

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')
