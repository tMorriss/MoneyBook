from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'moneybook_django',
        'USER': 'moneybook',
        'PASSWORD': 'want2money',
        'HOST': 'neptune.tmorriss.com',
        'PORT': '3306',
    }
}

APP_NAME = "MoneyBook"

ALLOWED_HOSTS = ['moneybook.tmorriss.com']