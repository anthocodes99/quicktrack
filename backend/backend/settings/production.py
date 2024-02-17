import dj_database_url
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [x.strip() for x in os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')]

if ALLOWED_HOSTS is None:
    raise Exception('Please set the environment variable DJANGO_ALLOWED_HOSTS!')

# SSL / CSRF / CSP

SECURE_SSL_REDIRECT = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

DEBUG_PROPAGATE_EXCEPTIONS = True

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
