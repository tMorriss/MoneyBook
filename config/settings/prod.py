from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'moneybook_django',
        'USER': 'moneybook',
        'PASSWORD': 'want2money',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

ALLOWED_HOSTS = ['moneybook.tmorriss.com']