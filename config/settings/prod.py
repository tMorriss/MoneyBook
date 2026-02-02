import os
from copy import deepcopy

from .common import *  # NOQA F403
from .common import LOGS_DIR

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
# Construct from ALLOWED_HOSTS with https:// scheme
_allowed_host = os.environ.get('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = [f'https://{_allowed_host}']

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

# 本番環境でも詳細なログを出力するための設定
# ファイルログを強化し、より多くの情報をキャプチャする
LOGGING = deepcopy(LOGGING)  # NOQA F405
LOGGING['handlers']['file']['filename'] = os.path.join(LOGS_DIR, 'moneybook_prod.log')
LOGGING['handlers']['file']['level'] = 'DEBUG'

# 本番環境では django.db.backends のログレベルを WARNING に設定して SQL クエリの出力を抑制
LOGGING['loggers']['django.db.backends']['level'] = 'WARNING'
