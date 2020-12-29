from .common import *  # NOQA F403
from .common import BASE_DIR
import os

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

APP_NAME = "dev-MoneyBook"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
