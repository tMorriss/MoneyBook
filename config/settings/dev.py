import os
from copy import deepcopy

from .common import *  # NOQA F403
from .common import BASE_DIR

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

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=8+4o-ub_b%m_rd4j+bgflxf48ucl-w6uoxr%ru50^m(*xm$5e'

# 開発環境のログ設定
LOGGING = deepcopy(LOGGING)  # NOQA F405
LOGGING['loggers']['django.db.backends']['level'] = 'DEBUG'
