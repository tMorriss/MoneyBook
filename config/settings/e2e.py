import os

from django.core.management.utils import get_random_secret_key

from .common import *  # NOQA F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'moneybook_e2e'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASS', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

APP_NAME = 'e2e-MoneyBook'

DEBUG = True

SECRET_KEY = get_random_secret_key()
