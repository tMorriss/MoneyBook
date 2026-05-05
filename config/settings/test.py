from .dev import *  # NOQA F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'OPTIONS': {
            'timeout': 30,
        },
    }
}

APP_NAME = 'test-MoneyBook'
